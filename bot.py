import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

MEMBER_ROLE_NAME = "MEMBERS"
WELCOME_CHANNEL_NAME = "Wellcome"
LEAVE_CHANNEL_NAME = "Leave"

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
            print(f"Assigned {MEMBER_ROLE_NAME} to {member.name}")
        except discord.Forbidden:
            print(f"Missing permissions to assign role to {member.name}")

    channel = discord.utils.get(member.guild.text_channels, name=WELCOME_CHANNEL_NAME)
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
    channel = discord.utils.get(member.guild.text_channels, name=LEAVE_CHANNEL_NAME)
    if channel:
        embed = discord.Embed(
            title="Goodbye!",
            description=f"**{member.name}** has left the server.",
            color=discord.Color.red()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        await channel.send(embed=embed)

import os

TOKEN = os.environ.get("DISCORD_TOKEN", "")
bot.run(TOKEN)
