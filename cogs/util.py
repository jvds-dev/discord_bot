import discord
from discord import app_commands
from discord.ext import commands

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name="ping", description="Mostra a latência do bot.")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"🏓 Pong! Latência: `{latency}ms`")
        
        
async def setup(bot):
    await bot.add_cog(Util(bot))