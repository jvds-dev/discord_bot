import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Bot conectado como {bot.user}")
        print(f"Slash commands sincronizados: {len(synced)}")
    except Exception as e:
        print(f"Erro ao sincronizar comandos: {e}")

@bot.tree.command(name="ping", description="Mostra a latência do bot.")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"🏓 Pong! Latência: `{latency}ms`")

bot.run(TOKEN)