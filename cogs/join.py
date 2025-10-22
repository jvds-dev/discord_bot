import discord
from discord.ext import commands
from discord import app_commands


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ────────────────────────────────
    # ENTRAR NO CANAL DE VOZ
    # ────────────────────────────────
    @app_commands.command(
        name="join",
        description="Conecta o bot ao canal de voz atual."
    )
    async def join(self, interaction: discord.Interaction):
        if not interaction.user.voice:
            await interaction.response.send_message(
                "❌ Você precisa estar em um canal de voz!", ephemeral=True
            )
            return

        channel = interaction.user.voice.channel
        await channel.connect()
        await interaction.response.send_message(
            f"🎤 Conectado em **{channel.name}**!"
        )

    # ────────────────────────────────
    # SAIR DO CANAL
    # ────────────────────────────────
    @app_commands.command(
        name="leave",
        description="Desconecta o bot do canal de voz."
    )
    async def leave(self, interaction: discord.Interaction):
        if not interaction.guild.voice_client:
            await interaction.response.send_message(
                "❌ Não estou em nenhum canal de voz.", ephemeral=True
            )
            return

        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("👋 Sai do canal de voz!")

    # ────────────────────────────────
    # TOCAR ÁUDIO
    # ────────────────────────────────
    @app_commands.command(
        name="play",
        description="Toca um áudio local no canal de voz."
    )
    async def play(self, interaction: discord.Interaction):
        voice_client = interaction.guild.voice_client
        if not voice_client:
            await interaction.response.send_message(
                "❌ O bot não está conectado a um canal de voz.", ephemeral=True
            )
            return

        source = discord.FFmpegPCMAudio("sounds/nggyu.mp3")
        voice_client.play(source, after=lambda e: print(f"Erro: {e}") if e else None)
        await interaction.response.send_message("🎶 Tocando som!")


async def setup(bot):
    await bot.add_cog(Voice(bot))
