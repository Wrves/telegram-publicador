# import asyncio
# import json
# import random
# from telethon.sync import TelegramClient
# #from telethon.errors import SessionPasswordNeededError

# async def main():
#     with open('config.json', 'r') as f:
#         config = json.load(f)

#     while True:
#         for cuenta in config['accounts']:
#             api_id = cuenta['api_id']
#             api_hash = cuenta['api_hash']
#             phone = cuenta['phone']
#             mensajes = cuenta['messages']
#             grupos = cuenta['groups']

#             print(f'Iniciando sesión para {phone}')
#             client = TelegramClient(f'session_{phone}', api_id, api_hash)

#             await client.connect()
#             if not await client.is_user_authorized():
#                 print(f"Cuenta {phone} no autorizada. Requiere autorización previa.")
#                 continue

#             for grupo in grupos:
#                 mensaje = random.choice(mensajes)
#                 try:
#                     await client.send_message(grupo, mensaje)
#                     print(f'Mensaje enviado desde {phone} a {grupo}')
#                     await asyncio.sleep(random.randint(1, 2))
#                 except Exception as e:
#                     print(f'Error con {phone} en {grupo}: {e}')

#             await client.disconnect()

#         await asyncio.sleep(random.randint(180, 240))  # Esperar 3–4 min

# asyncio.run(main())
import json
import asyncio
import random
from telethon import TelegramClient

# Leer el archivo de configuración
with open("config.json", encoding="utf-8") as f:
    config = json.load(f)

# Obtener los datos de la primera cuenta
cuenta = config["accounts"][0]
phone = cuenta["phone"]
api_id = cuenta["api_id"]
api_hash = cuenta["api_hash"]
grupos = cuenta["groups"]
mensajes = cuenta["messages"]

async def enviar_mensajes():
    async with TelegramClient(f"session_{phone}", api_id, api_hash) as client:
        while True:
            for grupo in grupos:
                for mensaje in mensajes:
                    try:
                        await client.send_message(grupo, mensaje)
                        print(f"✅ Mensaje enviado a {grupo}")
                    except Exception as e:
                        print(f"❌ Error enviando a {grupo}: {e}")
            espera = random.randint(120, 180)
            print(f"⏳ Esperando {espera} segundos antes del proximo envio...")
            await asyncio.sleep(espera)
# Ejecutar
asyncio.run(enviar_mensajes())
