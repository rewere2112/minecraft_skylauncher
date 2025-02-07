import tkinter as tk
import customtkinter as ctk
import minecraft_launcher_lib 
import os
import subprocess
import configparser
import shutil
import requests
import base64
import json
from io import BytesIO
from CTkMessagebox import CTkMessagebox 

# Crear archivo cache
config_file = 'config.ini'
minecraft_directory = f"C://Users//{os.environ['USERNAME']}//AppData//Roaming//.minecraft"
def insert_launcher_profiles():
    config = configparser.ConfigParser()
    config.read(config_file)
    if not config.has_section('SETUP'):
        config.add_section('SETUP')
        config.set('SETUP', 'launcher_profiles_inserted', 'False')
    if config.getboolean('SETUP', 'launcher_profiles_inserted') == False:
        source_file = 'path/to/launcher_profiles.jar'  # Update with the actual path to launcher_profiles.jar
        destination_file = os.path.join(minecraft_directory, 'launcher_profiles.jar')
        shutil.copy(source_file, destination_file)
        config.set('SETUP', 'launcher_profiles_inserted', 'True')
        with open(config_file, 'w') as configfile:
            config.write(configfile)

# Guardar la configuración
def save_config(username, version):
    config = configparser.ConfigParser()
    config['LAST_SESSION'] = {
        'username': username,
        'version': version
    }
    with open(config_file, 'w') as configfile:
        config.write(configfile)

# Cargar la configuración

def load_config():
    config = configparser.ConfigParser()
    config.read(config_file)
    if 'LAST_SESSION' in config:
        return config['LAST_SESSION']['username'], config['LAST_SESSION']['version']
    return '', ''

# Instalar Minecraft
def install_minecraft(version):
    minecraft_directory = f"C://Users//{os.environ['USERNAME']}//AppData//Roaming//.minecraft"
    minecraft_launcher_lib.install.install_minecraft_version(version, minecraft_directory)

#|  retornar uuid
def uuid(username):
    response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
    response.raise_for_status()
    uuid = response.json().get('id')
    if not uuid:
        raise ValueError("No se encontró el UUID en la respuesta.")
    return uuid

#|  retornar skin
def export_api_mojang2(uuid, username):
    profile_response = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}")
    profile_response.raise_for_status()
    properties = profile_response.json().get('properties', [])
    if not properties:
        raise ValueError("No se encontraron propiedades en la respuesta.")
    textures_value = properties[0].get('value')
    if not textures_value:
        raise ValueError("No se encontró el valor de las texturas en la respuesta.")
    decoded_textures = base64.b64decode(textures_value).decode('utf-8')
    textures_json = json.loads(decoded_textures)
    print(textures_json)
    return textures_json
    
def complete_login(client_id: str, client_secret: str | None, redirect_uri: str, auth_code: str, code_verifier: str | None = None) -> dict:
    {
            "id" : "The uuid",
            "name" : "The username",
            "access_token": "The acces token",
            "refresh_token": "The refresh token",
            "skins" : [{
                "id" : uuid,
                "state" : "ACTIVE",
                "url" : export_api_mojang2['textures']['SKIN']['url'],
                "variant" : "CLASSIC",
                "alias" : "STEVE"
            } ],
            "capes" : []
        }
# Lanzar Minecraft

def launch_minecraft(username, version):
    minecraft_directory = f"C://Users//{os.environ['USERNAME']}//AppData//Roaming//.minecraft"
    options = {
        "username": username,
        "uuid": uuid(username),
        "token": '',
        "jvmArguments": ["-Xmx4G", "-Xms4G"],
        "launcherVersion": "0.3"
        }
    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version, minecraft_directory, options)
    window.destroy()

    # Ejecutar minecraft
    subprocess.run(
        minecraft_command,
        creationflags=subprocess.CREATE_NO_WINDOW,  # Evita que se muestre la consola
        stdout=subprocess.DEVNULL,  # Descarta la salida estándar
       stderr=subprocess.DEVNULL   # Descarta los errores estándar
    )
    save_config(username, version)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------


# Crear la ventana principal
def main():
    # obtener versiones instaladas
    def get_installed_versions():
        return minecraft_launcher_lib.utils.get_installed_versions(minecraft_directory)
    # obtener versiones disponibles
    def get_available_versions():
        available_list = minecraft_launcher_lib.utils.get_version_list()
        return [version['id'] for version in available_list if version['type'] == 'release']
    # Actualizar la lista de versiones
    def update_listbox(selection):
        version_listbox.delete(0, ctk.END)
        if selection == "Versiones Instaladas":
            lista = get_installed_versions()
            for fort in lista:
                version_listbox.insert(ctk.END, fort['id'])
        elif selection == "Instalar mas versiones":
            lista = get_available_versions()
            for fort in lista:
                version_listbox.insert(ctk.END, fort)

    # configurar la apariencia de la ventana
    global window
    ctk.set_appearance_mode("system")  # Modo oscuro
    ctk.set_default_color_theme("green")  # Tema azul
    window = ctk.CTk()  # Crear ventana principal
    window.title("Minecraft Launcher 0.2")
    window.geometry("1024x576")
    window.resizable(False, False)  # Deshabilitar cambiar tamaño 

    # Obtener dimensiones de la pantalla y calcular posición centrada
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = 1024
    window_height = 576
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)

    # Establecer la geometría de la ventana con la posición calculada
    window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

     # Crear la cabecera
    header_frame = ctk.CTkFrame(window, height=120, width=window_width, fg_color="black")
    header_frame.place(x=0, y=0)  # Colocar la cabecera en la parte superior

    # Crear el frame del menú lateral
    menu_frame = ctk.CTkFrame(window, width=650)
    menu_frame.place(x=0, y=120, relheight=1.0) 
    # Crear el menú desplegable
    options = ["Versiones Instaladas", "Instalar mas versiones"]
    selected_option = ctk.StringVar(menu_frame)
    selected_option.set(options[0])  # Valor por defecto
    # Crear el menú desplegable
    dropdown = ctk.CTkOptionMenu(menu_frame, variable=selected_option, values=options, command=update_listbox, width=150, anchor="center", font=("Minecraft", 11))
    dropdown.pack(pady=5, padx=20, fill="both", expand=False, side="top", anchor="w")
    # Inicializar con la lista de versiones instaladas
    version_listbox = tk.Listbox(menu_frame, font=("Minecraft", 11), bg="#1F1F1F", fg="white", width=40, height=10, selectmode="single")
    version_listbox.config(highlightthickness=0, bd=15, relief="flat")
    version_listbox.pack_configure(padx=5, pady=10)
    version_listbox.pack(pady=5 , padx=1, fill="both", expand=True)

    update_listbox(options[0])
    # Función para actualizar version_entry
    def on_version_select(event):
        selected_version = version_listbox.get(version_listbox.curselection())
        version_entry.delete(0, tk.END)
        version_entry.insert(0, selected_version)

    # Vincular el evento de selección
    version_listbox.bind('<<ListboxSelect>>', on_version_select)
    
    # fondo
    # me dio pereza hacerlo
    # fin del fondo

    # Crear el frame principal
    # crear el campo de texto para el usuario
    username_label = ctk.CTkLabel(window, text="Usuario:", font=("Minecraft", 12), justify="center")
    username_label.pack(pady=(160,0), padx=(350, 0))

    username_entry = ctk.CTkEntry(window, font=("Minecraft", 12), width=200, justify="center")
    username_entry.pack(pady=5, padx=(350, 0))

    # Crear el campo de texto para la versión
    version_label = ctk.CTkLabel(window, text="Versión:", font=("Minecraft", 12))
    version_label.pack(pady=5, padx=(350, 0))

    version_entry = ctk.CTkEntry(window, font=("Minecraft", 12), width=200, justify="center")
    version_entry.pack(pady=5, padx=(350, 0))
    
    def messageboxinstall():
        CTkMessagebox(title="Instalación", message="La instalación ha sido exitosa",icon="check")
    
    def show_install_message_and_install():
        messageboxinstall()
        install_minecraft(version_entry.get())

    # Crear los botones de instalar y ejecutar
    install_button = ctk.CTkButton(window, text="Instalar", font=("Minecraft", 12), command=show_install_message_and_install)
    install_button.pack(pady=5, padx=(350, 0))

    # Crear el botón de ejecutar

    launch_button = ctk.CTkButton(window, text="Ejecutar", font=("Minecraft", 12), command=lambda: launch_minecraft(username_entry.get(), version_entry.get()))
    launch_button.pack(pady=5, padx=(350, 0))

    # Cargar la última configuración guardada
    last_username, last_version = load_config()
    username_entry.insert(0, last_username)
    version_entry.insert(0, last_version)

    # Iniciar el bucle principal de la interfaz
    window.mainloop()
# no se que es pero si no lo pongo no funciona
if __name__ == "__main__":
    main()

# dev by: risaygeo