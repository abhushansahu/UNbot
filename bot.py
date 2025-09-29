"""UN Discord Bot - Main Application"""
import discord
from discord.ext import commands
import logging
import os
import sys
from typing import Optional

from src.config import BOT_TOKEN, DEBUG
from src.data_manager import DataManager
from src.rate_limiter import RateLimiter
from src.commands import UNBotCommands

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True

bot = commands.Bot(
    command_prefix='!', 
    intents=intents,
    help_command=None,
    case_insensitive=True
)

# Initialize components
data_manager = DataManager()
rate_limiter = RateLimiter()
command_handler = UNBotCommands(data_manager, rate_limiter)

@bot.event
async def on_ready():
    """Bot ready event"""
    logger.info(f'{bot.user} has connected to Discord!')
    logger.info(f'Bot is in {len(bot.guilds)} guilds')
    print(f'🌍 UN Bot is online and ready to serve!')
    print(f'📊 Connected to {len(bot.guilds)} servers')

@bot.event
async def on_guild_join(guild):
    """Log when bot joins a new guild"""
    logger.info(f'Joined guild: {guild.name} (ID: {guild.id})')

@bot.event
async def on_guild_remove(guild):
    """Log when bot leaves a guild"""
    logger.info(f'Left guild: {guild.name} (ID: {guild.id})')

# Slash Commands
@bot.slash_command(
    name="charter",
    description="Retrieves and posts the full text of a specific UN Charter Article",
    options=[
        discord.Option(
            int,
            name="article",
            description="The article number to retrieve (1-999)",
            required=True,
            min_value=1,
            max_value=999
        )
    ]
)
async def charter(ctx, article: int):
    """Retrieve UN Charter article by number"""
    try:
        await command_handler.charter(ctx, article)
    except Exception as e:
        logger.error(f"Error in charter command: {e}")
        await ctx.respond("❌ An error occurred while retrieving the charter article. Please try again later.", ephemeral=True)

@bot.slash_command(
    name="resolution",
    description="Searches for and links to a specific Security Council or General Assembly resolution",
    options=[
        discord.Option(
            str,
            name="type",
            description="Resolution type",
            required=True,
            choices=[
                discord.OptionChoice(name="Security Council (SC)", value="sc"),
                discord.OptionChoice(name="General Assembly (GA)", value="ga")
            ]
        ),
        discord.Option(
            int,
            name="number",
            description="Resolution number",
            required=True,
            min_value=1,
            max_value=9999
        )
    ]
)
async def resolution(ctx, type: str, number: int):
    """Search for UN resolutions"""
    try:
        await command_handler.resolution(ctx, type, number)
    except Exception as e:
        logger.error(f"Error in resolution command: {e}")
        await ctx.respond("❌ An error occurred while searching for the resolution. Please try again later.", ephemeral=True)

@bot.slash_command(
    name="policy",
    description="Provides a brief, sourced definition/overview of a UN policy term",
    options=[
        discord.Option(
            str,
            name="term",
            description="The policy term to look up",
            required=True,
            max_length=50
        )
    ]
)
async def policy(ctx, term: str):
    """Get UN policy definition"""
    try:
        await command_handler.policy(ctx, term)
    except Exception as e:
        logger.error(f"Error in policy command: {e}")
        await ctx.respond("❌ An error occurred while retrieving the policy definition. Please try again later.", ephemeral=True)

@bot.slash_command(
    name="search",
    description="Search for UN Charter articles or policy terms",
    options=[
        discord.Option(
            str,
            name="query",
            description="Search query",
            required=True,
            max_length=100
        )
    ]
)
async def search(ctx, query: str):
    """Search for UN Charter articles or policy terms"""
    try:
        await command_handler.search(ctx, query)
    except Exception as e:
        logger.error(f"Error in search command: {e}")
        await ctx.respond("❌ An error occurred while searching. Please try again later.", ephemeral=True)

@bot.slash_command(
    name="latest",
    description="Posts a link and summary of the most recent official UN news update or Security Council session"
)
async def latest(ctx):
    """Get latest UN news and updates"""
    try:
        await command_handler.latest(ctx)
    except Exception as e:
        logger.error(f"Error in latest command: {e}")
        await ctx.respond("❌ An error occurred while retrieving the latest news. Please try again later.", ephemeral=True)

@bot.slash_command(
    name="help",
    description="Shows all available commands and their usage"
)
async def help_command(ctx):
    """Show help information"""
    try:
        await command_handler.help_command(ctx)
    except Exception as e:
        logger.error(f"Error in help command: {e}")
        await ctx.respond("❌ An error occurred while retrieving help. Please try again later.", ephemeral=True)

# Error handling
@bot.event
async def on_application_command_error(ctx, error):
    """Handle application command errors"""
    logger.error(f"Application command error in {ctx.command}: {error}")
    
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond(f"⏳ This command is on cooldown. Try again in {error.retry_after:.1f} seconds.", ephemeral=True)
    elif isinstance(error, commands.MissingPermissions):
        await ctx.respond("❌ You don't have permission to use this command.", ephemeral=True)
    elif isinstance(error, discord.HTTPException):
        if error.status == 429:
            await ctx.respond("⏳ Discord is rate limiting requests. Please try again later.", ephemeral=True)
        else:
            await ctx.respond("❌ A Discord API error occurred. Please try again later.", ephemeral=True)
    else:
        logger.error(f"Unhandled error: {error}", exc_info=True)
        await ctx.respond("❌ An unexpected error occurred. Please try again later.", ephemeral=True)

@bot.event
async def on_error(event, *args, **kwargs):
    """Handle general bot errors"""
    logger.error(f"Error in event {event}:", exc_info=True)

def main():
    """Main function to run the bot"""
    if not BOT_TOKEN:
        logger.error("DISCORD_TOKEN not found in environment variables")
        print("❌ DISCORD_TOKEN not found in environment variables")
        print("Please create a .env file with your Discord bot token")
        sys.exit(1)
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    logger.info("Starting UN Discord Bot...")
    try:
        bot.run(BOT_TOKEN)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()