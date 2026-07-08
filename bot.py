import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

MEMBER_ROLE_NAME = "Member"

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Bot is ready and watching for new members...")

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name=MEMBER_ROLE_NAME)
    if role is None:
        print(f'Role "{MEMBER_ROLE_NAME}" not found in server {member.guild.name}')
        return
    try:
        await member.add_roles(role, reason="Auto-assigned Member role on join")
        print(f"Assigned {MEMBER_ROLE_NAME} to {member.name}")
    except discord.Forbidden:
        print(f"Missing permissions to assign role to {member.name}")

import os

TOKEN = os.environ.get("DISCORD_TOKEN", "")
bot.run(TOKEN)
