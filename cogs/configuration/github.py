import discord
from discord.ext import commands, tasks
import requests
import json

# Assuming the bot version is stored in a config file
with open('config/config.json') as f:
    config = json.load(f)
bot_version = config.get("version")  # Current bot version

GITHUB_API_URL = "https://api.github.com/repos/tygocodes/jarb/releases/latest"

class GitHubVersionCheck(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.check_version.start()  # Start the task loop to check for version updates

    @tasks.loop(hours=24)  # Check every 24 hours
    async def check_version(self):
        response = requests.get(GITHUB_API_URL)
        if response.status_code == 200:
            latest_release = response.json()
            latest_version = latest_release["tag_name"]

            # Compare the latest version with the current version
            if latest_version != bot_version:
                # Find or create the "Logs" category
                guild = self.client.get_guild(config["guildID"])  # Assuming guildID is in config
                log_category = discord.utils.get(guild.categories, name="Logs")
                if not log_category:
                    log_category = await guild.create_category("Logs")

                # Find or create the "logs" channel
                log_channel = discord.utils.get(log_category.text_channels, name="github-repository")
                if not log_channel:
                    log_channel = await guild.create_text_channel(name="github-repository", category=log_category)

                # Send a message about the new version
                await log_channel.send(
                    f"New version available! The latest version is `{latest_version}`. You're currently using `{bot_version}`.\n"
                    f"Check it out here: {latest_release['html_url']}"
                )
        else:
            print(f"Failed to fetch the latest release from GitHub. Status code: {response.status_code}")

    @check_version.before_loop
    async def before_check_version(self):
        await self.client.wait_until_ready()  # Wait until the bot is ready before starting the loop

async def setup(client: commands.Bot) -> None:
    await client.add_cog(GitHubVersionCheck(client))
