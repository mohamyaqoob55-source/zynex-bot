import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

MEMBER_ROLE_NAME = "MEMBERS"

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Bot is ready and watching for new members...")

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name=MEMBER_ROLE_NAME)
    if role:
        try:
            await member.add_roles(role, reason="Auto-assigned Member role on join")
        except discord.Forbidden:
            pass

    channel = discord.utils.get(member.guild.text_channels, name="Wellcome")
    if not channel:
        channel = discord.utils.get(member.guild.text_channels, name="wellcome")
    if not channel:
        channel = discord.utils.get(member.guild.text_channels, name="welcome")
    if channel:
        embed = discord.Embed(
            title="Welcome!",
            description=f"Hey {member.mention}, welcome to **{member.guild.name}**!\nYou are member #{member.guild.member_count}.",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name="Leave")
    if not channel:
        channel = discord.utils.get(member.guild.text_channels, name="leave")
    if channel:
        embed = discord.Embed(
            title="Goodbye!",
            description=f"**{member.name}** has left the server.",
            color=discord.Color.red()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        await channel.send(embed=embed)

TOKEN = os.environ.get("DISCORD_TOKEN", "")
bot.run(TOKEN)
