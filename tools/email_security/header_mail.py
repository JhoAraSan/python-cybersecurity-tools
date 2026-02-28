import os
import json
import re
import hashlib
import requests
import tkinter as tk
from tkinter import filedialog
from email import policy
from email.parser import BytesParser
from email.utils import parsedate_to_datetime
from datetime import datetime
from bs4 import BeautifulSoup #pip install beautifulsoup4
from dotenv import load_dotenv #pip install python-dotenv ---> para cargar las variables de entorno
import ipaddress
import sys
from pathlib import Path
from datetime import timedelta, timezone

# ==================== CONFIGURACIÓN ====================
ENV_PATH = "assets/keys.env"
try:
    with open(ENV_PATH, 'r') as f:
        pass  # Solo para verificar que el archivo existe
except FileNotFoundError:
    msn=f"❌ Error: el archivo {ENV_PATH} no se encontró."
    print(msn)
    sys.exit(1)

load_dotenv(dotenv_path=ENV_PATH)
VT_API_KEY = os.getenv("VT_API_KEY")  # Guarda tu API Key de Virus Total en el archivo keys.env
JSON_TRACE_PATH = "tools\\email_security\\traza_virustotal.json"
JSON_CLAVES_PATH = "tools\\email_security\\claves_analisis.json"

# ==================== FUNCIONES DE UTILIDAD ====================

def cargar_traza():
    if os.path.exists(JSON_TRACE_PATH):
        with open(JSON_TRACE_PATH, 'r') as f:
            return json.load(f)
    return {'urls': {}, 'files': {}}

def guardar_traza(traza):
    with open(JSON_TRACE_PATH, 'w') as f:
        json.dump(traza, f, indent=4)

def cargar_claves():
    if os.path.exists(JSON_CLAVES_PATH):
        with open(JSON_CLAVES_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'phishing': [], 'publicidad': []}

def hashear_archivo(path):
    sha256 = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def analizar_url_virustotal(url, traza):
    if url in traza['urls']:
        return traza['urls'][url]

    headers = {'x-apikey': VT_API_KEY}
    data = {'url': url}
    response = requests.post('https://www.virustotal.com/api/v3/urls', headers=headers, data=data)
    if response.status_code == 200:
        analysis_id = response.json()['data']['id']
        result = requests.get(f"https://www.virustotal.com/api/v3/analyses/{analysis_id}", headers=headers).json()
        traza['urls'][url] = result
        return result
    else:
        return {'error': response.text}

def analizar_archivo_virustotal(sha256, traza):
    if sha256 in traza['files']:
        return traza['files'][sha256]

    headers = {'x-apikey': VT_API_KEY}
    url = f"https://www.virustotal.com/api/v3/files/{sha256}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        traza['files'][sha256] = result
        return result
    else:
        return {'error': response.text}

def extraer_urls(texto):
    urls = re.findall(r'https?://[\w\.-/\?=&%#]+', texto)
    return list(set(urls))

def extraer_urls_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    urls = [a.get('href') for a in soup.find_all('a', href=True)]
    iframes = [i.get('src') for i in soup.find_all('iframe', src=True)]
    scripts = [s.get('src') for s in soup.find_all('script', src=True)]
    return list(set(urls + iframes + scripts))

def evaluar_spoofing(headers, ip_pattern):
    spf = dkim = dmarc = "❓ No encontrado"
    ips = []
    for k in headers:
        if k.lower().startswith("authentication-results"):
            val = headers[k].lower()
            ips.extend(re.findall(ip_pattern, val))
            if 'spf=pass' in val:
                spf = "✅ Válido"
            elif 'spf=fail' in val or 'spf=softfail' in val:
                spf = "❌ Falló"

            if 'dkim=pass' in val:
                dkim = "✅ Válido"
            elif 'dkim=fail' in val:
                dkim = "❌ Falló"

            if 'dmarc=pass' in val:
                dmarc = "✅ Válido"
            elif 'dmarc=fail' in val or 'dmarc=none' in val:
                dmarc = "❌ Falló"
    return spf, dkim, dmarc, ips

def detectar_publicitario(texto, from_):
    claves = cargar_claves().get('publicidad', [])
    if any(palabra in texto.lower() for palabra in claves):
        return True
    if any(alias in from_.lower() for alias in ['noreply', 'info', 'newsletter']):
        return True
    return False

def detectar_phishing_por_texto(texto):
    patrones = cargar_claves().get('phishing', [])
    if any(palabra in texto.lower() for palabra in patrones):
        return True
    return any(re.search(pat, texto) for pat in patrones)

def obtener_veredicto(total_detecciones, spf, dkim, dmarc, urls, adjuntos, es_publicitario, es_phishing):
    if es_phishing:
        return "❗ Posiblemente malicioso"
     
    if es_publicitario and total_detecciones == 0:
        return "⚠️ Sin amenazas técnicas, pero es publicitario no solicitado"

    score = 0
    score += total_detecciones
    score += 3 if spf == "❌ Falló" else 0
    score += 3 if dkim == "❌ Falló" else 0
    score += 3 if dmarc == "❌ Falló" else 0
    score += len([u for u in urls if 'bit.ly' in u or 'tinyurl' in u])
    score += len([a for a in adjuntos if a.lower().endswith(('.js', '.exe', '.docm', '.vbs'))])

    if score >= 5:
        return "❗ Posiblemente malicioso"
    elif score >= 3:
        return "⚠️ Este correo presenta señales de posible fraude"
    else:
        return "✅ Sin señales directas de amenaza"

def procesar_correo(path, traza, output_dir, resumen_global, resumen_estadisticas, correo_reportar):
    with open(path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)

    headers = dict(msg.items())
    # Obtener la fecha y convertirla a datetime, luego ajustar a GMT-5
    date_header = msg['Date']
    if date_header:
        try:
            date_obj = parsedate_to_datetime(date_header)
            # Ajustar a GMT-5 (restar 5 horas)
            gmt_minus_5 = timezone(timedelta(hours=-5))
            date_obj = date_obj.astimezone(gmt_minus_5)
            # Formatear la fecha
            date = date_obj.strftime("%a, %d %b %Y %H:%M:%S (GMT-5)")
        except Exception:
            date = date_header
    else:
        date = "Desconocida"
    subject = msg['Subject']
    from_ = msg['From']
    reply_to = msg['Reply-To']
    received_spf =msg["Received-SPF"]
    return_path = headers.get('Return-Path')
    filename = os.path.basename(path)

    # ---- Deteccion de IPS de envio
    received_headers = msg.get_all("Received")
    ips_re = []

    # Tomar el último (origen más cercano al emisor)
    origin_header = received_headers[-1]

    # Regex que detecta IPv4
    ip_pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"

    for header in reversed(received_headers):
        ips = re.findall(ip_pattern, header)
        for ip in ips:
            try:
                ip_obj = ipaddress.ip_address(ip)
                if not ip_obj.is_private:
                    ips_re.append(ip)
                    break
            except ValueError:
                continue
    # ----

    body_text = ""
    body_html = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body_text += part.get_content()
            elif part.get_content_type() == "text/html":
                body_html += part.get_content()
    else:
        if msg.get_content_type() == "text/plain":
            body_text = msg.get_content()
        elif msg.get_content_type() == "text/html":
            body_html = msg.get_content()

    urls_text = extraer_urls(body_text)
    urls_html = extraer_urls_html(body_html)
    urls = list(set(urls_text + urls_html))

    url_info = []
    total_detecciones = 0
    for url in urls:
        result = analizar_url_virustotal(url, traza)
        stats = result.get('data', {}).get('attributes', {}).get('stats', {})
        detections = stats.get('malicious', 0)
        total_detecciones += detections
        url_info.append((url, detections))

    adjuntos = []
    adjunto_info = []
    for part in msg.iter_attachments():
        nombre = part.get_filename()
        if not nombre:
            continue
        payload = part.get_payload(decode=True)
        ruta_adjunto = os.path.join(output_dir, nombre)
        with open(ruta_adjunto, 'wb') as f:
            f.write(payload)
        hash_arch = hashear_archivo(ruta_adjunto)
        resultado = analizar_archivo_virustotal(hash_arch, traza)
        stats = resultado.get('data', {}).get('attributes', {}).get('last_analysis_stats', {})
        detecciones = stats.get('malicious', 0)
        total_detecciones += detecciones
        adjuntos.append(nombre)
        adjunto_info.append((nombre, hash_arch, detecciones))

    spf, dkim, dmarc, ips_val = evaluar_spoofing(headers,ip_pattern)
    es_publicitario = detectar_publicitario(body_text, from_)
    es_phishing = detectar_phishing_por_texto(body_text)
    veredicto = obtener_veredicto(total_detecciones, spf, dkim, dmarc, urls, adjuntos, es_publicitario, es_phishing)

    resumen_estadisticas[veredicto] = resumen_estadisticas.get(veredicto, 0) + 1
    if not veredicto== "✅ Sin señales directas de amenaza":
        correo_reportar.extend([from_]) if from_ not in correo_reportar else None

    informe = [
        f"📬 Archivo: {filename}",
        f"📅 Fecha del mensaje: {date}",
        f"🧑 Remitente: {from_}",
        f"📝 Asunto: {subject}",
        f"📎 Adjuntos: {', '.join(adjuntos) if adjuntos else 'Ninguno'}\n",
        f"🔍 Veredicto: {veredicto}",
        "🧠 Comentario: Análisis automático basado en reputación de enlaces, adjuntos, autenticación y estructura.\n",
    ]

    if es_publicitario:
        informe.append("📣 Observación: Este correo parece ser una promoción o invitación comercial no solicitada.")
        informe.append("➡️ Recomendación: Puede ser descartado si no fue solicitado por el usuario.\n")

    if url_info:
        informe.append("🔗 Enlaces encontrados:")
        for url, detecciones in url_info:
            estado = "✅ Limpio" if detecciones == 0 else f"❗ Detectado por {detecciones} motores"
            if len(url) > 50:
                url = url[:47] + "..."
            informe.append(f"- {url} → {estado}")
        informe.append("")

    informe.append("🔐 Validaciones de seguridad:")
    informe.append(f"- SPF: {spf}")
    informe.append(f"- DKIM: {dkim}")
    informe.append(f"- DMARC: {dmarc}")
    informe.append(f"- From vs Reply-To: {'⚠️ Diferente' if reply_to and reply_to != from_ else '✅ Coinciden'}")
    informe.append(f"- From vs Return-Path: {'⚠️ Diferente' if return_path and return_path != from_ else '✅ Coinciden'}\n")
    informe.append("🧩 Análisis heurístico:")
    ips_unicas=list(set(ips_re + ips_val))
    informe.append(f"- {len(ips_unicas)} direcciones IP encontradas: {ips_unicas}")
    informe.append(f"- Recived-SPF: {received_spf if received_spf else 'No encontrado'}")


    if adjunto_info:
        informe.append("📦 Hash de adjuntos:")
        for nombre, hash_arch, det in adjunto_info:
            estado = "✅ Limpio" if det == 0 else f"❗ Detectado por {det} motores"
            informe.append(f"- {nombre} → SHA256: {hash_arch} → {estado}")

    informe.append("\n" + ("="*60) + "\n")
    resumen_global.extend(informe)
    print(f"✅ Procesado: {filename}")

def seleccionar_y_procesar():
    downloads_path = Path.home() / "Downloads" if (Path.home() / "Downloads").exists() else Path.home()

    root = tk.Tk()
    root.withdraw()
    archivos = filedialog.askopenfilenames(initialdir=downloads_path, title="Selecciona archivos .eml", filetypes=[("EML files", "*.eml")])
    if not archivos:
        return

    carpeta_salida = filedialog.askdirectory(initialdir=downloads_path,title="Selecciona carpeta de salida")
    if not carpeta_salida:
        return

    resumen_global = []
    correo_reportar = []
    correo_reportar.extend(["📧 Correos a reportar:"])
    resumen_estadisticas = {}
    traza = cargar_traza()
    carpeta_adjuntos = os.path.join(carpeta_salida, "adjuntos")
    os.makedirs(carpeta_adjuntos, exist_ok=True)
    for archivo in archivos:
        procesar_correo(archivo, traza, carpeta_adjuntos, resumen_global, resumen_estadisticas, correo_reportar)

    guardar_traza(traza)
    # Encabezado con correos a reportar
    correo_reportar.extend(["-"*60 + "\n"])
    # Encabezado con resumen estadístico
    encabezado = ["📊 Resumen del análisis:"]
    for clave, valor in resumen_estadisticas.items():
        encabezado.append(f"- {clave}: {valor} correo(s)")
    encabezado.append("\n📝 El detalle de cada análisis se describe a continuación:\n")
    encabezado.append("="*60 + "\n")

    timestamp = datetime.now().strftime("%d-%b-%Y_%H.%M")
    nombre_archivo = f"informe_{timestamp}.txt"
    ruta_salida = os.path.join(carpeta_salida, nombre_archivo)

    with open(ruta_salida, 'w', encoding='utf-8') as f:
        f.write('\n'.join(correo_reportar + encabezado + resumen_global))

    print(f"\n📄 Informe consolidado generado: {ruta_salida}")
    print("🎉 Todos los correos fueron analizados.")

if __name__ == "__main__":
    seleccionar_y_procesar()
