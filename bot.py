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
    for guild in bot.guilds:
        print(f"Server: {guild.name}")
        for ch in guild.text_channels:
            print(f"  Channel: #{ch.name}")

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name=MEMBER_ROLE_NAME)
    if role:
        try:
            await member.add_roles(role, reason="Auto-assigned Member role on join")
        except discord.Forbidden:
            pass

    for ch in member.guild.text_channels:
        if "welcome" in ch.name.lower() or "wellcome" in ch.name.lower():
            embed = discord.Embed(
                title="Welcome!",
                description=f"Hey {member.mention}, welcome to **{member.guild.name}**!\nYou are member #{member.guild.member_count}.",
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            await ch.send(embed=embed)
            return
    print(f"No welcome channel found in {member.guild.name}")

@bot.event
async def on_member_remove(member):
    for ch in member.guild.text_channels:
        if "leave" in ch.name.lower():
            embed = discord.Embed(
                title="Goodbye!",
                description=f"**{member.name}** has left the server.",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            await ch.send(embed=embed)
            return
    print(f"No leave channel found in {member.guild.name}")

TOKEN = os.environ.get("DISCORD_TOKEN", "")
bot.run(TOKEN)
