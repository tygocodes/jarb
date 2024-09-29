import discord
from discord.ext import commands
from discord.ui import Button, View
import json

with open('config/config.json') as f:
    config = json.load(f)

class SetupView(View):
    def __init__(self, client: commands.Bot):
        super().__init__(timeout=None)
        self.client = client  # Store the client object for access within buttons

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green, custom_id="setup_yes")
    async def yes_button(self, interaction: discord.Interaction, button: Button):
        guildid = 1283795487899648071
        guild = self.client.get_guild(guildid)

        # Update the setup status in the config file
        with open('config/config.json') as f:
            setup_data = json.load(f)
            setup_data["setup"] = "True"
            with open('config/config.json', 'w') as f:
                json.dump(setup_data, f, indent=4)

        await interaction.response.send_message("You clicked 'Yes'. Your bot will be set up automatically.", ephemeral=True)

        # Create or get the "Logs" category
        logCategory = discord.utils.get(guild.categories, name="Logs")
        if not logCategory:
            logCategory = await guild.create_category("Logs")
            
            setup_channel = await guild.create_text_channel(
                name="github-repository", 
                category=logCategory
            )
        # Create or get the "Tickets" category
        ticketCategory = discord.utils.get(guild.categories, name="Tickets")
        if not ticketCategory:
            ticketCategory = await guild.create_category("Tickets")


    @discord.ui.button(label="No", style=discord.ButtonStyle.red, custom_id="setup_no")
    async def no_button(self, interaction: discord.Interaction, button: Button):
        with open('config/config.json') as f:
            setup_data = json.load(f)
            setup_data["setup"] = "Manually"
            with open('config/config.json', 'w') as f:
                json.dump(setup_data, f, indent=4)   
        await interaction.response.send_message("You clicked 'No'. Your bot will not be set up automatically.", ephemeral=True)

class SetupCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        # Check if the bot setup is required
        if config.get("setup") == "False":
            guildid = 1283795487899648071
            guild = self.client.get_guild(guildid)

            if guild is None:
                print(f"Error: Could not find guild with ID {guildid}. Please verify the guild ID.")
                return  # Exit if the guild can't be found

            # Find or create the "jarb" category
            category = discord.utils.get(guild.categories, name="jarb")
            if not category:
                category = await guild.create_category("jarb")

            # Create the setup text channel under the "jarb" category
            setup_channel = await guild.create_text_channel(
                name="jarb-setup", 
                category=category
            )

            # Create the message with buttons
            view = SetupView(self.client)  # Create a view with the buttons
            embed = discord.Embed(
                title="Jarb Setup",
                description=f"Hello {guild.owner.mention},\n\nThank you for inviting me to your server! It looks like this is my first time here, and I need to be set up. You have the option to configure everything manually, but we highly recommend the automatic setup for a smoother experience. Let's get started!",
                color=discord.Color.gold()
            )
            embed.add_field(name="Automatic Setup", value="Click the 'Yes' button to automatically configure Jarb for you.")
            embed.add_field(name="Manual Setup", value="Click the 'No' button to manually configure Jarb for you.")

            await setup_channel.send(
                embed=embed,
                view=view
            )

async def setup(client: commands.Bot) -> None:
    await client.add_cog(SetupCog(client))
