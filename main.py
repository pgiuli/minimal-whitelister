import discord
from discord.ext import commands
from discord import app_commands

import users

import os
#Load variables from .env file
from dotenv import load_dotenv
load_dotenv()

token = os.getenv("DISCORD_TOKEN")
role_id = int(os.getenv("MEMBER_ROLE_ID"))


description = '''A bot to whitelist users on a minecraft server'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)
        print("Failed to sync commands")


@bot.tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!", ephemeral=True)

@bot.tree.command(name="whitelist")
async def whitelist(interaction: discord.Interaction, username: str):
    print(f"Whitelist {username} by user {interaction.user.display_name}")
    response = users.whitelist(interaction.user.id, username)

    role = interaction.guild.get_role(role_id)
    print(role)
    if response != "Username already in use by another player!" and role not in interaction.user.roles:
        await interaction.user.add_roles(role, reason="Whitelisted on minecraft server")

    await interaction.response.send_message(response, ephemeral=True)
    

@bot.tree.command(name="unwhitelist")
async def unwhitelist(interaction: discord.Interaction):
    print(f"Unwhitelist by user {interaction.user.display_name}")
    print(interaction.user.id)

    role = interaction.guild.get_role(role_id)
    if role in interaction.user.roles:
        await interaction.user.remove_roles(role, reason="Unwhitelisted on minecraft server")

    response = users.unwhitelist(interaction.user.id)
    await interaction.response.send_message(response, ephemeral=True)


bot.run(token)