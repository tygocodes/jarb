import discord
from discord.ext import commands
from discord import app_commands
import json
from datetime import datetime

with open("config/config.json") as f:
    config = json.load(f)

launch_time = datetime.now()

class test(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    

    test = app_commands.Group(name="test", description="test")

    @test.command(name="ping", description="pong")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.client.latency * 1000)  # Convert to milliseconds
        
        time = f"<t:{int(launch_time.timestamp())}:R>"

        embed = discord.Embed(title='Ping and Uptime', color=discord.Color.green())
        embed.add_field(name='Latency', value=f'{latency}ms', inline=False)
        embed.add_field(name='Uptime', value=time, inline=False)

        await interaction.response.send_message(embed=embed)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(test(client))