import discord
from discord.ext import commands
import os
import unicodedata

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

MEMBER_ROLE_NAME = "MEMBERS"

def clean(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c)).lower()

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

    for ch in member.guild.text_channels:
        if "wel" in clean(ch.name):
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
        if "lea" in clean(ch.name):
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
