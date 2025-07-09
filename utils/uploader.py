import os
import requests
import discord

MAX_DISCORD_FILESIZE = 10 * 1024 * 1024  # 10 MB

async def upload_or_attach(interaction, filepath):
    try:
        file_size = os.path.getsize(filepath)

        if file_size <= MAX_DISCORD_FILESIZE:
            await interaction.followup.send(file=discord.File(filepath))
        else:
            with open(filepath, 'rb') as f:
                response = requests.post("https://file.io", files={"file": f})

            if response.status_code == 200:
                data = response.json()
                url = data.get("link")
                if url:
                    await interaction.followup.send(
                        f"🚫 El archivo pesa más de 10 MB y no se puede subir directo a Discord.\n"
                        f"📎 Pero tranqui, lo subí acá para vos:\n{url}"
                    )
                else:
                    await interaction.followup.send("❌ No se pudo obtener el link de file.io.")
            else:
                await interaction.followup.send("❌ Error al subir el archivo a file.io.")
    except Exception as e:
        await interaction.followup.send(f"❌ Error al manejar el archivo: `{e}`")
