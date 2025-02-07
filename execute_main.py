import os
import shutil
import getpass
import subprocess

def copiar_archivo_y_abrir_exe():
    try:
        # 1. Obtener la ruta del directorio donde se encuentra main.py
        ruta_actual = os.path.dirname(os.path.abspath(__file__))
        print(f"El archivo main.py está en: {ruta_actual}")

        # 2. Ruta del archivo launcher_profiles.json en la misma carpeta
        ruta_origen = os.path.join(ruta_actual, "launcher_profiles.json")

        # 3. Obtener el nombre de usuario del sistema
        usuario = getpass.getuser()

        # 4. Ruta de destino en AppData\Roaming\.minecraft
        ruta_destino = os.path.join("C:\\Users", usuario, "AppData", "Roaming", ".minecraft", "launcher_profiles.json")

        # Verificar si el archivo de origen existe
        if os.path.exists(ruta_origen):
            # Crear la carpeta de destino si no existe
            os.makedirs(os.path.dirname(ruta_destino), exist_ok=True)
            
            # Copiar el archivo a la ruta de destino
            shutil.copy(ruta_origen, ruta_destino)
            print(f"Archivo copiado exitosamente a: {ruta_destino}")

            # 5. Abrir el archivo main.exe
            ruta_exe = os.path.join(ruta_actual, "main.exe")
            if os.path.exists(ruta_exe):
                print(f"Abriendo {ruta_exe}...")
                subprocess.Popen(ruta_exe)  # Abre el archivo .exe
            else:
                print(f"El archivo {ruta_exe} no existe.")
        else:
            print(f"El archivo de origen no existe: {ruta_origen}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

# Ejecutar la función
copiar_archivo_y_abrir_exe()

