import discord
import random
import asyncio
from discord import app_commands
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="coinflip", description="Joga uma moeda que pode cair cara ou coroa.")
    async def coinflip(self, interaction: discord.Interaction):
        await interaction.response.defer()

        msg_animation = [
            "A moeda está no ar .",
            "A moeda está no ar . .",
            "A moeda está no ar . . .",
        ]

        await interaction.edit_original_response(content=msg_animation[0])

        for i in range(1, len(msg_animation)):
            await asyncio.sleep(0.7)
            await interaction.edit_original_response(content=msg_animation[i])

        result = random.choice(["Cara", "Coroa"])
        await asyncio.sleep(0.5)
        await interaction.edit_original_response(content=f"🪙 A moeda caiu **`{result}`**!")

async def setup(bot):
    await bot.add_cog(Fun(bot))
