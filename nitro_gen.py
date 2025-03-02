import discord
from discord import app_commands
import random
import string
from time import localtime, strftime
import asyncio  # Import for adding a delay between messages

TOKEN = "1344740224021958769"
GUILD_ID = 1345818474265448519 # Replace with your server ID

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        await self.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f'Logged in as {self.user}')

client = MyClient()

@client.tree.command(name="generate", description="Generates one or multiple Discord Nitro codes", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(code_type="Choose the type of code: basic or boost", count="Number of codes to generate (max 10)")
async def generate(interaction: discord.Interaction, code_type: str, count: int = 1):
    if code_type not in ["basic", "boost"]:
        await interaction.response.send_message("Invalid type! Use 'basic' or 'boost'.", ephemeral=True)
        return
    
    if count < 1 or count > 10:
        await interaction.response.send_message("Invalid number! Choose between 1 and 10.", ephemeral=True)
        return

    await interaction.response.defer()  # Indicate that the response will take some time
    
    length = 24 if code_type == "boost" else 16

    for _ in range(count):
        code = f"discord.gift/{''.join(random.choices(string.ascii_letters + string.digits, k=length))}"
        timestamp = strftime('%H:%M', localtime())
        await interaction.followup.send(f"[{timestamp}] {code}")
        await asyncio.sleep(1.5)  # Add a 1.5-second delay between each message

client.run(TOKEN)
