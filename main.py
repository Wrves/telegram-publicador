
# import json
# import asyncio
# import random
# from telethon import TelegramClient

# # Leer el archivo de configuración
# with open("config.json", encoding="utf-8") as f:
#     config = json.load(f)

# # Obtener los datos de la primera cuenta
# cuenta = config["accounts"][0]
# phone = cuenta["phone"]
# api_id = cuenta["api_id"]
# api_hash = cuenta["api_hash"]
# grupos = cuenta["groups"]
# mensajes = cuenta["messages"]

# async def enviar_mensajes():
#     async with TelegramClient(f"session_{phone}", api_id, api_hash) as client:
#         while True:
#             for grupo in grupos:
#                 for mensaje in mensajes:
#                     try:
#                         await client.send_message(grupo, mensaje)
#                         print(f"✅ Mensaje enviado a {grupo}")
#                     except Exception as e:
#                         print(f"❌ Error enviando a {grupo}: {e}")
#             espera = random.randint(120, 180)
#             print(f"⏳ Esperando {espera} segundos antes del proximo envio...")
#             await asyncio.sleep(espera)
# # Ejecutar
# asyncio.run(enviar_mensajes())


import json
import os
import asyncio
import random
from telethon import TelegramClient
from telethon.sessions import StringSession

SESSION_DIR = "sessions"
os.makedirs(SESSION_DIR, exist_ok=True)

print_lock = asyncio.Lock()  # Para sincronizar prints y evitar mezcla

# Leer configuración
with open("config.json", encoding="utf-8") as f:
    config = json.load(f)

# Función para manejar cada cuenta individualmente
async def manejar_cuenta(cuenta):
    phone = cuenta["phone"]
    api_id = cuenta["api_id"]
    api_hash = cuenta["api_hash"]
    grupos = cuenta["groups"]
    mensajes = cuenta["messages"]

    session_path = os.path.join(SESSION_DIR, f"session_{phone.replace('+', '')}.session")
    client = TelegramClient(session_path, api_id, api_hash)

    await client.connect()
    if not await client.is_user_authorized():
        try:
            await client.send_code_request(phone)
            code = input(f"🔑 Ingresa el código que recibiste en {phone}: ")
            await client.sign_in(phone, code)
        except Exception as e:
            print(f"❌ Error al iniciar sesión con {phone}: {e}")
            await client.disconnect()
            return
        print(f"✅ Sesión iniciada para {phone}")
    else: 
        print(f"🔐 Sesión existente reutilizada para {phone}")
        
    try:
        while True:
            logs = [f"📨 Envíos para cuenta {phone}:"]
            for grupo in grupos:
                for mensaje in mensajes:
                    try:
                        if not client.is_connected():
                            await client.connect()
                        await client.send_message(grupo, mensaje)
                        logs.append(f" - Grupo {grupo}: ✅ éxito")
                        # print(f"📨 {phone} envio mensaje a {grupo}")
                    except Exception as e:
                        logs.append(f" - Grupo {grupo}: ❌ error: {e}")
                        # print(f"❌ {phone} Error en {grupo}: {e}")
            espera = random.randint(120, 180)
            logs.append(f"⏳ {phone} esperando {espera} segundos para la siguiente ronda...\n")
            # print(f"⏳ {phone} esperando {espera} segundos para siguiente ronda")
            async with print_lock:
                print("\n".join(logs))
                
            await asyncio.sleep(espera)
    except Exception as e:
            print(f"❗ Error general con {phone}: {e}")
    

# Ejecutar todas las cuentas en paralelo
async def main():
    tareas = [manejar_cuenta(cuenta) for cuenta in config["accounts"]]
    await asyncio.gather(*tareas)

if __name__ == "__main__":
    asyncio.run(main())
