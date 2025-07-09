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
            await interaction.followup.send("📤 El archivo pesa más de 10MB. Subiéndolo a GoFile...")

            # Paso 1: obtener el server
            server_resp = requests.get("https://api.gofile.io/getServer").json()
            server = server_resp["data"]["server"]

            # Paso 2: subir el archivo
            with open(filepath, "rb") as f:
                upload_resp = requests.post(
                    f"https://{server}.gofile.io/uploadFile",
                    files={"file": f}
                ).json()

            # Paso 3: revisar si todo ok y enviar link
            if upload_resp["status"] == "ok":
                download_page = upload_resp["data"]["downloadPage"]
                await interaction.followup.send(
                    f"✅ Archivo subido a GoFile:\n{download_page}"
                )
            else:
                await interaction.followup.send(
                    f"❌ Error al subir el archivo a GoFile. Respuesta: {upload_resp}"
                )

    except Exception as e:
        await interaction.followup.send(f"❌ Error al manejar el archivo: `{e}`")
