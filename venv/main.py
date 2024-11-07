import discord
import os
from typing import Final
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

class Client(commands.Bot):
    # Runs whenever the bot starts up
    async def on_ready(self):
        print(f"{self.user} is here!")         

    async def on_message (self, message):
        # The bot won't respond to its own messages
        if message.author == self.user:
            return

intents = discord.Intents.default()
intents.message_content = True

client = Client(command_prefix = "!", intents = intents)

# Bot answers with "Hello" when using "/hello" command
@client.tree.command(name="hello", description="Says hello back")
async def sayHello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello")

# Bot prints whatever the user tells them to print
@client.tree.command(name="copycat", description="Will print what you say back")
async def copyCat(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(message)

# Creates a role with name and colour by HEX (wihout #)
@client.tree.command(name="create_role", description="Creating new role (HEX w/o #)")
async def createRole(interaction: discord.Interaction, role_name: str, color: str = "ffffff"):
    # Stores the required role in the variable 
    requiredRole = discord.utils.get(interaction.guild.roles, name="*")
    # Checks if the user has the required role to use the command
    if requiredRole in interaction.user.roles:
        try: 
            # Stores existing roles
            tempRole = discord.utils.get(interaction.guild.roles)
            # Checks if role name is already existing
            if tempRole in interaction.guild.roles:
                await interaction.response.send_message(f"Role `{role_name}` already exists")
            # If it doesn't exist it will create the role
            else: 
                color = discord.Color(int(color, 16))
                role = await interaction.guild.create_role(name = role_name, color = color)
                await interaction.response.send_message(f"Role `{role_name}` has been created")

        except Exception as e:
            print(f"An error occurred: {e}")  
    else:
        await interaction.response.send_message("You don't have permission")

# Deletes a role by the name
@client.tree.command(name="delete_role", description="Deletes a role")
async def deleteRole(interaction: discord.Interaction, role_name: str):
    # Stores the required role in the variable 
    requiredRole = discord.utils.get(interaction.guild.roles, name="*")
    # Checks if the user has the required role to use the command
    if requiredRole in interaction.user.roles:
        role = discord.utils.get(interaction.guild.roles, name = role_name)
        # Checks if role exists
        if role:
            try:
                # Delete role if found
                await role.delete()
                await interaction.response.send_message(f"Role `{role_name}` has been deleted")
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            # Tells user the role is not found
            await interaction.response.send_message(f"Role `{role_name}` was not found")
    else:
        await interaction.response.send_message("You don't have permission")

# Edit a role name and colour
@client.tree.command(name="edit_role", description="Edit a role name and colour")
async def editRole(interaction: discord.Interaction, role_name: str, new_role_name:str, color: str = "ffffff"):
    # Stores the required role in the variable 
    requiredRole = discord.utils.get(interaction.guild.roles, name="*")
    # Checks if the user has the required role to use the command
    if requiredRole in interaction.user.roles:
        role = discord.utils.get(interaction.guild.roles, name = role_name)
        # If the role exists it will change it
        if role:
            try:
                color = discord.Color(int(color, 16))
                await role.edit(name=new_role_name, color=color)
                # Notifies the user the role has been changed
                await interaction.response.send_message(f"Role `{role_name}` has been changed to {new_role_name}.")
            except Exception as e:
                # Tells user the role is not found
                await interaction.response.send_message(f"Role `{role_name}` was not found")
    else:
        await interaction.response.send_message("You don't have permission")

# Create a voice channel when user enters the "Create Voice" voice channel
@client.event
async def on_voice_state_update(member, before, after):
    # Checks if anyone is in "Create Room" voice channel
    if after.channel and after.channel.name == "Create Room":
        guild = member.guild
        # Creates a new voice called "{user}'s Room"
        new_channel = await guild.create_voice_channel(name=f"{member.display_name}'s Room", category=discord.utils.get(guild.categories, name="Voice Channels"))
        # Moves to user there
        await member.move_to(new_channel)
        # Checks if user left, then deletes channel
        def check_voice_state(m, b, a):
            return m == member and a.channel != new_channel
        
        await client.wait_for("voice_state_update", check=check_voice_state)
        await new_channel.delete()

# Discord token
load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
client.run(token = TOKEN)
