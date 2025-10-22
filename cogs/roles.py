import discord
from discord.ext import commands
from discord import app_commands


class RoleSelect(discord.ui.Select):
    def __init__(self, roles: list[discord.Role]):
        options = [
            discord.SelectOption(label=role.name, value=str(role.id))
            for role in roles
        ]

        super().__init__(
            placeholder="Escolha seus cargos...",
            min_values=1,
            max_values=len(roles),
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        self.view.selected_roles = [int(v) for v in self.values]
        # print(self.view.selected_roles)
        await interaction.response.defer()

class ConfirmButton(discord.ui.Button):
    def __init__(self):
       super().__init__(label="✅ Confirmar", style=discord.ButtonStyle.success)
    
    async def callback(self, interaction: discord.Interaction):
        selected_ids = getattr(self.view, "selected_roles", [])
        if not selected_ids:
            await interaction.response.send_message(
                "⚠️ Nenhum cargo selecionado!", ephemeral=True
            )
            return

        roles_to_add = [
            interaction.guild.get_role(rid) for rid in selected_ids
            if interaction.guild.get_role(rid)
        ]
        
        added, removed = [], []
        for role in roles_to_add:
            if role not in interaction.user.roles:
                await interaction.user.add_roles(role)
                added.append(role.name)
            else:
                await interaction.user.remove_roles(role)
                removed.append(role.name)
                       
            
        embed = discord.Embed(
            title="🎭 Cargos atualizados",
            description="Suas modificações foram aplicadas com sucesso!",
            color=discord.Color.green()
        )
       
        if added:
            embed.add_field(
                name="✅ Adicionados",
                value=", ".join(added),
                inline=False
            )
        if removed:
            embed.add_field(
                name="❎ Removidos",
                value=", ".join(removed),
                inline=False
            )
            
        embed.set_footer(text=f"Solicitado por {interaction.user.display_name}", icon_url=interaction.user.display_avatar)
        
        await interaction.response.edit_message(embed=embed, view=None)
        
        # await interaction.response.edit_message(
        #     content=f"✅ Cargos modificados: {', '.join(msg_parts)}",
        #     view=None
        # )
    

class RoleMenu(discord.ui.View):
    def __init__(self, roles: list[discord.Role], author_id: int):
        super().__init__(timeout=None)
        self.selected_roles = []
        self.author_id = author_id
        self.add_item(RoleSelect(roles))
        self.add_item(ConfirmButton())
        
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(
                "❌ Apenas quem executou o comando pode usar este menu.",
                ephemeral=True
            )
            return False
        return True


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="roles", description="Permite que os usuários escolham cargos do servidor."
    )
    async def roles(self, interaction: discord.Interaction):
        allowed_channel_id = 1430266317008797767
        
        if interaction.channel_id != allowed_channel_id:
            await interaction.response.send_message(
            f"❌ Este comando só pode ser usado em <#{allowed_channel_id}>!",
            ephemeral=True
            )
            return
        
        role_ids = [
            1429943777539264602,
            1429943934708224100,
            1429944010809802854,
        ]

        roles = [
            interaction.guild.get_role(rid)
            for rid in role_ids
            if interaction.guild.get_role(rid)
        ]
        if not roles:
            await interaction.response.send_message(
                "⚠️ Nenhum cargo configurado!", ephemeral=True
            )
            return

        view = RoleMenu(roles, interaction.user.id)
        await interaction.response.send_message(
            "🎭 Escolha seus cargos abaixo:", view=view, ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(Roles(bot))
