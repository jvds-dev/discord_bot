import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # 👈 necessário para on_member_join funcionar


bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")
    
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"🔹 Cog carregado: {filename}")

    try:
        synced = await bot.tree.sync()
        print(f"📦 Slash commands sincronizados: {len(synced)}")
    except Exception as e:
        print(f"⚠️ Erro ao sincronizar comandos: {e}")

bot.run(TOKEN)
