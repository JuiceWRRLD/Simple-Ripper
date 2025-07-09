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

            if response.status_code == 200:
                data = response.json()
                url = data["data"]["downloadPage"]
                await interaction.followup.send(
                    f"🚫 El archivo pesa más de 10MB y no se puede subir directo a Discord.\n"
                    f"📎 Lo subí por vos acá:\n{url}"
                )
            else:
                await interaction.followup.send("❌ Error al subir el archivo a GoFile.")

    except Exception as e:
        await interaction.followup.send(f"❌ Error al manejar el archivo: `{e}`")
