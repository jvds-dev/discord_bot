import discord
from discord import app_commands
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import aiohttp
import io
import os

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        welcome_channel_id = 1430268023398338672
        channel = member.guild.get_channel(welcome_channel_id)
        if not channel:
            return
        
        bg_path = "assets/welcome_bg.png"
        background = Image.open(bg_path).convert("RGBA")
        
        avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
        async with aiohttp.ClientSession() as session:
            async with session.get(avatar_url) as resp:
                avatar_bytes = await resp.read()
        
        avatar = Image.open(io.BytesIO(avatar_bytes)).convert("RGBA")
        avatar = avatar.resize((100, 100))
        
        mask = Image.new("L", avatar.size, 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, avatar.size[0], avatar.size[1]), fill=255)
        
        avatar_round = Image.new("RGBA", avatar.size)
        avatar_round.paste(avatar, (0, 0), mask=mask)
                
        background.paste(avatar_round, (149, 25), avatar_round)
        
        image_bytes = io.BytesIO()
        background.save(image_bytes, format="PNG")
        image_bytes.seek(0)
        
        await channel.send(
            content=f"🎉 Bem-vindo(a) ao servidor, {member.mention}!",
            file=discord.File(image_bytes, filename="welcome.png"),
        )
    
    @app_commands.command(name="welcome_teste", description="Simula a mensagem de boas-vindas.")
    async def welcome_teste(self, interaction: discord.Interaction):
        welcome_channel_id = 1430268023398338672
        channel = interaction.guild.get_channel(welcome_channel_id)
        if not channel:
            return
        
        bg_path = "assets/welcome_bg.png"
        background = Image.open(bg_path).convert("RGBA")
        
        avatar_url = interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url
        async with aiohttp.ClientSession() as session:
            async with session.get(avatar_url) as resp:
                avatar_bytes = await resp.read()
        
        avatar = Image.open(io.BytesIO(avatar_bytes)).convert("RGBA")
        avatar = avatar.resize((100, 100))
        
        mask = Image.new("L", avatar.size, 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, avatar.size[0], avatar.size[1]), fill=255)
        
        avatar_round = Image.new("RGBA", avatar.size)
        avatar_round.paste(avatar, (0, 0), mask=mask)
                
        background.paste(avatar_round, (149, 25), avatar_round)
           
        image_bytes = io.BytesIO()
        background.save(image_bytes, format="PNG")
        image_bytes.seek(0)
        
        await channel.send(
            content=f"🎉 Bem-vindo(a) ao servidor, {interaction.user.mention}!",
            file=discord.File(image_bytes, filename="welcome.png"),
        )
        # if channel:
        #     await channel.send(
        #         f"🎉 Seja bem-vindo(a) ao servidor, {interaction.user.mention}! "
        #         f"Fique à vontade e leia as regras."
        #     )
        #     await interaction.response.send_message("✅ Mensagem de boas-vindas enviada!", ephemeral=True)
        # else:
        #     await interaction.response.send_message("⚠️ Canal de boas-vindas não encontrado!", ephemeral=True)

            
async def setup(bot):
    await bot.add_cog(Welcome(bot))