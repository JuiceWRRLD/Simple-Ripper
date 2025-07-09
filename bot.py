import discord
from discord import app_commands
from discord.ext import commands
import os
import asyncio
from downloaders import youtube, soundcloud, instagram, tiktok, x
from utils import cleaner
from utils.uploader import upload_or_attach  # ✅ NUEVO IMPORT

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"SIMPLE RIPPER está online como {bot.user}!")
    try:
        synced = await bot.tree.sync()
        print(f"Comandos slash sincronizados: {len(synced)}")
    except Exception as e:
        print(e)

@bot.tree.command(name="rip", description="Descarga música o video desde una URL")
@app_commands.describe(url="Link de YouTube, TikTok, SoundCloud o Instagram")
async def rip(interaction: discord.Interaction, url: str):
    await interaction.response.defer()
    await interaction.followup.send("🔍 Procesando...")
    try:
        file_path, file_name = None, None

        if "youtube.com" in url or "youtu.be" in url:
            file_path, file_name = youtube.download(url)
        elif "soundcloud.com" in url:
            file_path, file_name = soundcloud.download(url)
        elif "tiktok.com" in url:
            file_path, file_name = tiktok.download(url)
        elif "instagram.com" in url:
            file_path, file_name = instagram.download(url)
        elif "x.com" in url or "twitter.com" in url:
            await interaction.followup.send("⏬ Descargando desde X...")
            file_path, file_name = x.download(url)
        else:
            await interaction.followup.send("❌ Plataforma no soportada.")
            return

        await upload_or_attach(interaction, file_path)  # ✅ NUEVO
        cleaner.clean_temp(file_path)

    except Exception as e:
        await interaction.followup.send(f"❌ Error: {str(e)}")

@bot.tree.command(name="rip_vid", description="Descarga video desde una URL de YouTube")
@app_commands.describe(url="Link de YouTube")
async def rip_vid(interaction: discord.Interaction, url: str):
    await interaction.response.defer()
    await interaction.followup.send("🔍 Procesando video...")
    try:
        file_path, file_name = youtube.download_video(url)
        await upload_or_attach(interaction, file_path)  # ✅ NUEVO
        cleaner.clean_temp(file_path)

    except Exception as e:
        await interaction.followup.send(f"❌ Error: {str(e)}")

@bot.tree.command(name="rip_soundcloud", description="Descargar audio de SoundCloud a 320kbps")
async def rip_soundcloud(interaction: discord.Interaction, url: str):
    await interaction.response.defer()
    try:
        await interaction.followup.send("🎵 Descargando desde SoundCloud...")
        file_path, file_name = soundcloud.download(url)
        await upload_or_attach(interaction, file_path)  # ✅ NUEVO
        cleaner.clean_temp(file_path)

    except Exception as e:
        await interaction.followup.send(f"❌ Error: {str(e)}")

@bot.tree.command(name="rip_x", description="Descargar video desde X (Twitter)")
async def rip_x(interaction: discord.Interaction, url: str):
    await interaction.response.defer()
    try:
        await interaction.followup.send("⏬ Descargando desde X...")
        file_path, file_name = x.download(url)
        await upload_or_attach(interaction, file_path)  # ✅ NUEVO
        cleaner.clean_temp(file_path)

    except Exception as e:
        await interaction.followup.send(f"❌ Error: {str(e)}")

@bot.tree.command(name="rip_tiktok", description="Descargar video de TikTok")
async def rip_tiktok(interaction: discord.Interaction, url: str):
    await interaction.response.defer()
    try:
        await interaction.followup.send("📱 Descargando desde TikTok...")
        file_path, file_name = tiktok.download(url)
        await upload_or_attach(interaction, file_path)  # ✅ NUEVO
        cleaner.clean_temp(file_path)

    except Exception as e:
        await interaction.followup.send(f"❌ Error: {str(e)}")

@bot.tree.command(name="rip_ig", description="Descargar video o imagen de Instagram")
async def rip_ig(interaction: discord.Interaction, url: str):
    await interaction.response.defer()
    try:
        await interaction.followup.send("📸 Descargando desde Instagram...")
        file_path, file_name = instagram.download(url)
        await upload_or_attach(interaction, file_path)  # ✅ NUEVO
        cleaner.clean_temp(file_path)

    except Exception as e:
        await interaction.followup.send(f"❌ Error: {str(e)}")

import os
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
