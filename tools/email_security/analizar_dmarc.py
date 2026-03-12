
import os
import gzip
import csv
import xml.etree.ElementTree as ET
from tkinter import Tk
from tkinter.filedialog import askdirectory
from Info_Ip import ip_isp

def extract_failed_ips(directory):
    failed_ips = []
    cont=0
    
    for filename in os.listdir(directory):
        if filename.endswith(".xml.gz"): # Verifica si el archivo es un .xml.gz
            filepath = os.path.join(directory, filename) # Ruta completa del archivo
            with gzip.open(filepath, 'rt', encoding='utf-8') as f: # Abre el archivo gzip
                try:
                    tree = ET.parse(f)
                    root = tree.getroot()
                    if root.tag != 'feedback' or root.find('report_metadata') is None:
                        print(f"Archivo no válido: {filename}")
                        continue
                    
                    for record in root.findall('record'):
                        cont+=1
                        source_ip = record.find('row/source_ip').text
                        dkim_result = record.find('auth_results/dkim/result').text if record.find('auth_results/dkim/result') is not None else 'none'
                        spf_result = record.find('auth_results/spf/result').text if record.find('auth_results/spf/result') is not None else 'none'
                        if dkim_result != 'pass' or spf_result != 'pass':
                            failed_ips.append((source_ip, dkim_result, spf_result))
                except ET.ParseError:
                    print(f"Error al parsear el archivo: {filename}")
    return failed_ips, cont

def export_to_csv(failures, output_file):
    ips = set()
    datos=[]
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['IP', 'DKIM Result', 'SPF Result', 'ISP'])
        # escribir las ips fallidas sin repetir
        for ip, dkim, spf in failures:
            if ip not in ips:
                ips.add(ip)
                datos.append((ip, dkim, spf))
        for ip, dkim, spf in datos:
            isp = ip_isp(ip)
            writer.writerow([ip, dkim, spf, isp])

# Selección de carpeta con GUI
root = Tk()
root.withdraw() # Oculta la ventana principal
directorio = askdirectory(title="Selecciona la carpeta con archivos .xml.gz")

if directorio:
    archivo_salida = os.path.join(directorio, "fallos_dmarc.csv")
    fallos, total = extract_failed_ips(directorio)
    export_to_csv(fallos, archivo_salida)
    print(f"✅ Resultados exportados a: {archivo_salida}, {total} registros procesados.")
else:
    print("❌ No se seleccionó ninguna carpeta.")
