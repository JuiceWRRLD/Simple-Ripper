import os
import requests
import discord

MAX_DISCORD_FILESIZE = 10 * 1024 * 1024  # 10 MB

def upload_to_gofile(filepath):
    try:
        # Pedimos el server
        server_resp = requests.get(
            "https://api.gofile.io/getServer",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        server = server_resp.json()["data"]["server"]

        # Subimos el archivo
        with open(filepath, "rb") as f:
            upload_resp = requests.post(
                f"https://{server}.gofile.io/uploadFile",
                files={"file": f}
            ).json()

        if upload_resp["status"] == "ok":
            return upload_resp["data"]["downloadPage"]
        else:
            print(f"[GoFile Error] {upload_resp}")
            return None

    except Exception as e:
        print(f"[GoFile Exception] {e}")
        return None

def upload_to_krakenfiles(filepath):
    try:
        with open(filepath, 'rb') as f:
            response = requests.post(
                "https://krakenfiles.com/api/upload",
                files={"file": f}
            )

        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                return data["data"]["file"]["url"]
            else:
                print(f"[KrakenFiles Error] {data}")
                return None
        else:
            print(f"[KrakenFiles HTTP Error {response.status_code}] {response.text}")
            return None

    except Exception as e:
        print(f"[KrakenFiles Exception] {e}")
        return None

async def upload_or_attach(interaction, filepath):
    try:
        file_size = os.path.getsize(filepath)

        if file_size <= MAX_DISCORD_FILESIZE:
            await interaction.followup.send(file=discord.File(filepath))
        else:
            await interaction.followup.send("📤 Archivo grande. Subiendo a GoFile...")

            link = upload_to_gofile(filepath)
            if not link:
                await interaction.followup.send("⚠️ GoFile falló. Probando con KrakenFiles...")
                link = upload_to_krakenfiles(filepath)

            if link:
                await interaction.followup.send(f"✅ Archivo subido:\n{link}")
            else:
                await interaction.followup.send("❌ No se pudo subir el archivo a ningún host.")

    except Exception as e:
        await interaction.followup.send(f"❌ Error al manejar el archivo: `{e}`")
