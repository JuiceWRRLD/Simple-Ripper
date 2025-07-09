import os
import requests
import discord

MAX_DISCORD_FILESIZE = 10 * 1024 * 1024  # 10 MB
GOFILE_API = "https://api.gofile.io/uploadFile"

async def upload_or_attach(interaction, filepath):
    try:
        file_size = os.path.getsize(filepath)

        if file_size <= MAX_DISCORD_FILESIZE:
            await interaction.followup.send(file=discord.File(filepath))
        else:
            await interaction.followup.send("📤 Subiendo archivo a GoFile...")

            with open(filepath, 'rb') as f:
                response = requests.post(GOFILE_API, files={"file": f})

            # 👇 Agregamos este print para debug
            print(f"[DEBUG] GoFile response status: {response.status_code}")
            print(f"[DEBUG] GoFile response text: {response.text}")

            if response.status_code == 200:
                data = response.json()
                url = data["data"]["downloadPage"]
                await interaction.followup.send(
                    f"📎 El archivo pesa más de 10MB. Lo subí acá:\n{url}"
                )
            else:
                await interaction.followup.send(
                    f"❌ Error al subir el archivo a GoFile. Código {response.status_code}.\n"
                    f"📄 Respuesta: {response.text}"
                )

    except Exception as e:
        await interaction.followup.send(f"❌ Error al manejar el archivo: `{e}`")
