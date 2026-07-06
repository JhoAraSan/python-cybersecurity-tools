from pathlib import Path
import tkinter as tk
from tkinter import filedialog,messagebox
import win32com.client as win32


# ==========================================
# Selección de archivos/carpetas
# ==========================================

def seleccionar_carpeta():
    root = tk.Tk()
    root.withdraw()

    carpeta = filedialog.askdirectory(
        title="Seleccione la carpeta que contiene los Excel"
    )

    if not carpeta:
        return []

    carpeta = Path(carpeta)

    archivos = [
        f for f in carpeta.rglob("*")
        if f.is_file()
        and not f.name.startswith("~$")
        and f.suffix.lower() in (".xlsx", ".xlsm", ".xls")
    ]

    return archivos


def seleccionar_archivos():
    root = tk.Tk()
    root.withdraw()

    archivos = filedialog.askopenfilenames(
        title="Seleccione uno o varios Excel",
        filetypes=[
            ("Archivos Excel", "*.xlsx *.xlsm *.xls")
        ]
    )

    return [Path(f) for f in archivos]


# ==========================================
# Procesamiento
# ==========================================

def configurar_paginas(wb, excel):
    for hoja in wb.Worksheets:

        ps = hoja.PageSetup

        ps.Orientation = 2

        ps.Zoom = False
        ps.FitToPagesWide = 1
        ps.FitToPagesTall = False

        ps.LeftMargin = excel.CentimetersToPoints(0.3)
        ps.RightMargin = excel.CentimetersToPoints(0.3)
        ps.TopMargin = excel.CentimetersToPoints(0.3)
        ps.BottomMargin = excel.CentimetersToPoints(0.3)

        ps.HeaderMargin = excel.CentimetersToPoints(0.2)
        ps.FooterMargin = excel.CentimetersToPoints(0.2)

        ps.CenterHorizontally = True


def convertir_excel_a_pdf(ruta_excel, excel):

    ruta_pdf = ruta_excel.with_suffix(".pdf")

    if ruta_pdf.exists():
        print(f"PDF ya existe: {ruta_pdf.name}")
        return True

    wb = None

    try:

        print(f"\nProcesando: {ruta_excel}")

        wb = excel.Workbooks.Open(
            str(ruta_excel),
            UpdateLinks=0,
            ReadOnly=True,
            IgnoreReadOnlyRecommended=True
        )

        configurar_paginas(wb, excel)

        wb.ExportAsFixedFormat(
            Type=0,
            Filename=str(ruta_pdf),
            Quality=0,
            IncludeDocProperties=True,
            IgnorePrintAreas=True,
            OpenAfterPublish=False
        )

        print(f"PDF creado: {ruta_pdf.name}")

        return True

    except Exception as e:

        print(f"ERROR: {ruta_excel.name}")
        print(e)

        raise

    finally:

        if wb is not None:
            try:
                wb.Close(False)
            except:
                pass


def procesar_archivos(lista_archivos):

    excel = win32.gencache.EnsureDispatch("Excel.Application")

    excel.Visible = False
    excel.DisplayAlerts = False
    excel.AskToUpdateLinks = False

    procesados = 0
    errores = []

    try:

        for archivo in lista_archivos:

            try:
                convertir_excel_a_pdf(archivo, excel)
                procesados += 1

            except Exception as e:
                errores.append(f"{archivo} -> {e}")

    finally:

        try:
            excel.Quit()
        except:
            pass

    return procesados, errores


# ==========================================
# Menú principal
# ==========================================

def main():

    usar_carpeta = messagebox.askyesno(
    "Modo de selección",
    "¿Desea seleccionar una carpeta?\n\nSí = Carpeta\nNo = Archivos")

    if usar_carpeta:
        archivos = seleccionar_carpeta()
    else:
        archivos = seleccionar_archivos()


    if not archivos:
        print("No se seleccionaron archivos.")
        return

    procesados, errores = procesar_archivos(archivos)

    print("\n====================")
    print(f"PDF generados: {procesados}")
    print(f"Errores: {len(errores)}")

    if errores:

        print("\nERRORES:")

        for error in errores:
            print(error)

    print("\nProceso terminado.")


if __name__ == "__main__":
    main()