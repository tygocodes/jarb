import discord
from discord import app_commands
from discord.ext import commands, tasks
import json
from colorama import Back, Fore, Style
import time
import platform
import os

with open("config/config.json") as f:
    config = json.load(f)


class aclient(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('.'), intents=discord.Intents.all())
        self.cogslist = ["cogs.configuration.testing", "cogs.configuration.setup"]
        self.synced = False
        self.added = False
    
    async def setup_hook(self):
        for ext in self.cogslist:
            await self.load_extension(ext)
            print(f"Loaded extension: {ext}")

        

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await client.tree.sync(guild = discord.Object(id=config["guildID"]))
            self.synced = True
        if not self.added:
            self.added = True
        prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S >", time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
        print(prfx + " Logged in as " + Fore.YELLOW + self.user.name)
        print(prfx + " Bot ID " + Fore.YELLOW + str(self.user.id))
        print(prfx + " Discord Version " + Fore.YELLOW + discord.__version__)
        print(prfx + " Python Version " + Fore.YELLOW + str(platform.python_version()))
        synced = await self.tree.sync()
        print(prfx + " Slash CMDs Synced " + Fore.YELLOW + str(len(synced)) + " Commands")
        

client = aclient()

client.run(config["appToken"])