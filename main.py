import asyncio
import json
import random
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError

async def main():
    with open('config.json', 'r') as f:
        config = json.load(f)

    while True:
        for cuenta in config['cuentas']:
            api_id = cuenta['api_id']
            api_hash = cuenta['api_hash']
            phone = cuenta['phone']
            mensajes = cuenta['mensajes']
            grupos = cuenta['grupos']

            print(f'Iniciando sesión para {phone}')
            client = TelegramClient(f'session_{phone}', api_id, api_hash)

            await client.connect()
            if not await client.is_user_authorized():
                print(f"Cuenta {phone} no autorizada. Requiere autorización previa.")
                continue

            for grupo in grupos:
                mensaje = random.choice(mensajes)
                try:
                    await client.send_message(grupo, mensaje)
                    print(f'Mensaje enviado desde {phone} a {grupo}')
                    await asyncio.sleep(random.randint(1, 2))
                except Exception as e:
                    print(f'Error con {phone} en {grupo}: {e}')

            await client.disconnect()

        await asyncio.sleep(random.randint(180, 240))  # Esperar 3–4 min

asyncio.run(main())
