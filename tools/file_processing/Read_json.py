import json

with open('bitwarden_export_20260202192852.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

vistos = set()
resultado = []

for item in data['items']:
    clave = (item.get("name"), item.get("username"), item.get("password"))

    if clave not in vistos:
        vistos.add(clave)
        resultado.append(item)

print(f'habian: {len(data["items"])} elementos. Se eliminaron {len(data["items"]) - len(resultado)} elementos duplicados. y quedaron {len(resultado)} elementos sin duplicados.')

with open("datos_sin_duplicados.json", "w", encoding="utf-8") as f:
    json.dump(resultado, f, indent=4, ensure_ascii=False)