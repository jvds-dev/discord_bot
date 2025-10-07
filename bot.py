import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import random
import asyncio

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

@bot.tree.command(name="coinflip", description="Joga uma moeda que pode cair cara ou coroa.")
async def coinflip(interaction: discord.Interaction):
    await interaction.response.defer()

    msg_animation = [
        "A moeda está no ar .",
        "A moeda está no ar . .",
        "A moeda está no ar . . ."
    ]
    
    await interaction.edit_original_response(content=msg_animation[0])
    
    for i in range(1, len(msg_animation)):
        await asyncio.sleep(0.7)
        await interaction.edit_original_response(content=msg_animation[i])

    result = random.choice(["Cara", "Coroa"])
    await asyncio.sleep(0.5)
    await interaction.edit_original_response(
        content=f"🪙 A moeda caiu **`{result}`**!"
    )

bot.run(TOKEN)