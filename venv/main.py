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
        try: 
            guild = discord.Object(id=1303886816537088081)
            synced = await self.tree.sync(guild = guild)
            print(f"Synced {len(synced)} commands to guild {guild.id}")

        except Exception as e:
            print(f"Error syncing commands: {e}")
            

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


# Discord token
load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
client.run(token = TOKEN)