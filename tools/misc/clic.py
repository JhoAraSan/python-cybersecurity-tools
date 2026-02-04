# version 3 mas rapido

import pyautogui #pip install PyAutoGUI --> this install pyperclip and pymsgbox
import pyperclip as clipboard #pip install pyperclip
from pynput import keyboard, mouse  #pip install pynput
import time
import datetime
import os
from tkinter import messagebox as MessageBox
from tkinter.filedialog import asksaveasfile
import json

pyautogui.FAILSAFE = False
SAFE_MARGIN = 10

def check_abort():
    x, y = pyautogui.position()
    if x < SAFE_MARGIN and y < SAFE_MARGIN:
        raise KeyboardInterrupt

def clics_pegar():
    """
    Perform clicks and paste a list of cases.
    """
    print("\033[32mIngrese el listado de Casos:\033[39m") #INGRESO DE URL'S
    list = []  #ARREGLO DE URL
    while True:
        inputs = input()
        if inputs:
            list.append(inputs)
        else:
            break
    print("\033[32mPunto para 'Add Ticket'")
    input()
    px, py = pyautogui.position()
    print("\033[32mPunto para primer Ticket\033[35m")
    input()
    pxd, pyd = pyautogui.position()
    time.sleep(1)
    x = 0
    for caso in list:
        if x == 0:
            pyautogui.moveTo(pxd, pyd)
            pyautogui.click()
            clipboard.copy(caso)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.3)
            x += 1
            continue
        pyautogui.moveTo(px, py, 1)
        pyautogui.click()
        time.sleep(0.3)
        if x == 10:
            MessageBox.showwarning("Finish", "Acepte las condiciones \n(Ojo, primero acepte en FM, luego acepte esta ventana emergente!!!)")
            pyautogui.moveTo(px, py)
            pyautogui.click()
            time.sleep(0.3)
            clipboard.copy(caso)
            pyautogui.hotkey('ctrl', 'v')
            x += 1
            continue
        clipboard.copy(caso)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.3)
        x += 1
        print(progressbar(x, len(list)), end='\r')
    MessageBox.showwarning("Finish", 'Finalizado')

def clics():
    """
    Perform clicks at multiple points for a specified number of times.
    """
    try:
        puntos = int(input("\033[35mCuantos puntos? \033[39m"))
        t = round(float(input("\033[32m tiempo de transición entre ciclo en segundos (ej: 5.2)?\033[39m ")),1)
        count_input= input("¿Cuántas veces [letra v], cuantas horas [h] o cuantos minutos [m]? (ej: 30v o 0.5h o 30m): ").lower().strip()
        if count_input.endswith('v'):
            count = int(count_input[:-1])
        elif count_input.endswith('h'):
            hours = float(count_input[:-1])
            count = int(hours * 3600 * 0.75 / (t + 0.5 * puntos))  # considerando 0.5 segundos de movimiento por punto)
        elif count_input.endswith('m'):
            minutes = float(count_input[:-1])
            count = int(minutes * 60 * 0.75 / (t + 0.5 * puntos)) # el 0.75 es un factor de seguridad para cubrir tiempos adicionales

    except ValueError:
        print("Entrada inválida. Asegúrese de ingresar números correctos.")
        return
    posiciones =[]
    print(f"\033[35m la cantidad de ciclos es: {count}, con un tiempo por ciclo de {t} segundos \033[39m")
    for x in range(1, puntos + 1):
        print("\033[36mPunto ", str(x), " para el mouse\033[35m")
        input()
        px, py = pyautogui.position()
        posiciones.append((px, py))
    hora_ini = datetime.datetime.now().replace(microsecond=0)

    for x in range(count):
        for p in posiciones:
            xp, yp = p
            pyautogui.moveTo(xp, yp, 0.5) # 0.5 segundos de movimiento
            pyautogui.click()
        time.sleep(t)   
        hora_actual = datetime.datetime.now().replace(microsecond=0)
        print(progressbar(x, count), end='\r')
    MessageBox.showwarning("Finish", f'empezo a las:{hora_ini}, para un total de {hora_actual - hora_ini} tiempo')

def clics_copiar():
    """
    Copy URLs from a specified number of cases.
    """
    print("\033[35mCuantas URLS desea copiar \033[39m") #INGRESO DE URL'S
    x = int(input())
    list =''
    print("Punto para 'url'")
    input()
    px, py = pyautogui.position()
    print("Punto para 'Dismiss''\033[32m")
    input()
    pxd, pyd = pyautogui.position()
    time.sleep(0.3)
    for caso in range(x):
        pyautogui.moveTo(px, py)
        pyautogui.click()
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'c')
        url = clipboard.paste()
        list = list + f'{url}\n'
        time.sleep(0.3)
        pyautogui.moveTo(pxd, pyd)
        pyautogui.click()
        time.sleep(1)
        print(progressbar(caso, x), end='\r')
    save(list)

def save(list): 
    """
    Save the list of URLs to a file.
    """
    files = [('CSV Files', '*.csv'),  
             ('All Files', '*.*')] 
    file = asksaveasfile(filetypes = files, defaultextension = files)
    file.write(list)
    file.close()

def progressbar(part, total):
    """
    Generate a progress bar based on the current progress and total count.
    """
    frac = part / total
    completed = int(frac * 30)
    miss = 30 - completed
    bar = f"[{'#'* completed}{'-'* miss}]{frac:.1%}"
    return bar

def grabar_macro():
    print("\033[32mTenga en cuenta hacer la macro en la pantalla principal\033[39m")
    print("\033[32mGrabando... Presione ESC para finalizar\033[39m")

    events = []
    last_time = time.time()

    def save_event(event_type, data):
        nonlocal last_time
        now = time.time()
        events.append({
            "type": event_type,
            "data": data,
            "delay": now - last_time
        })
        last_time = now

    def on_press(key):
        if key == keyboard.Key.esc:
            return False
        save_event("key_down", {"key": str(key)})

    def on_release(key):
        save_event("key_up", {"key": str(key)})

    def on_click(x, y, button, pressed):
        save_event("mouse_click", {
            "x": x, "y": y,
            "button": str(button),
            "pressed": pressed
        })

    with keyboard.Listener(on_press=on_press, on_release=on_release) as kl, \
         mouse.Listener(on_click=on_click) as ml:
        kl.join()
        ml.stop()

    with open("macro.json", "w") as f:
        json.dump(events, f, indent=2)

    MessageBox.showwarning("Finish", "Macro grabada correctamente")

def reproducir_macro():
    if not os.path.exists("macro.json"):
        MessageBox.showerror("Error", "No existe macro grabada")
        return
    try:
        veces = input("\033[32m¿Cuántas veces desea reproducir la macro? \033[39m")
    except ValueError:
        MessageBox.showerror("Error", "Entrada inválida")
        return
    try:
        with open("macro.json") as f:
            events = json.load(f)
        print("\033[32mReproduciendo macro...\033[39m")
        for _ in range(int(veces)):
            for e in events:
                time.sleep(e["delay"])

                if e["type"] == "mouse_click":
                    if e["data"]["pressed"]:
                        pyautogui.mouseDown(e["data"]["x"], e["data"]["y"])
                    else:
                        pyautogui.mouseUp(e["data"]["x"], e["data"]["y"])

                elif e["type"] == "key_down":
                    pyautogui.keyDown(e["data"]["key"].replace("'", ""))

                elif e["type"] == "key_up":
                    pyautogui.keyUp(e["data"]["key"].replace("'", ""))

    except KeyboardInterrupt:
        MessageBox.showwarning(
            "Abortado",
            "Macro detenida manualmente (zona segura)"
        )


if __name__ == '__main__':
    while True:
        try:
            os.system('cls')
            print("\033[32mSeleccione una opción:\033[39m")
            print("""
                1) Dar clics n veces
                2) Enviar listado de casos
                3) Clean News
                4) Grabar macro (ESC para parar)
                5) Reproducir macro
                6) Salir
                """)

            entrada = int(input("\033[32mOpcion 1 al 6?: \033[39m"))
            match entrada:
                case 1:clics()
                case 2:clics_pegar()
                case 3:clics_copiar()
                case 4:grabar_macro()
                case 5:reproducir_macro()
                case 6:
                    print("\n\033[32m\033[45mNospi!\033[39m\033[49m")
                    os.system('cmd exit()')
                    break
                case _:
                    print("Seleccion inválida. Inténtalo nuevamente.")
                    continue
        except ValueError:
            print("Entrada inválida. Inténtalo nuevamente.")
        except KeyboardInterrupt:
            print("\n\nComenzemos de Nuevo!\n")
            continue
