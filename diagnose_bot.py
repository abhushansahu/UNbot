#!/usr/bin/env python3
"""Diagnose Discord bot issues"""
import asyncio
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

async def diagnose_bot():
    """Diagnose bot connection and permissions"""
    print("🔍 Diagnosing Discord Bot...")
    
    # Check token
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("❌ DISCORD_TOKEN not found in .env file")
        return
    
    print(f"✅ Token found: {token[:10]}...")
    
    # Create bot with minimal intents
    intents = discord.Intents.default()
    intents.guilds = True
    
    bot = commands.Bot(command_prefix='!', intents=intents)
    
    @bot.event
    async def on_ready():
        print(f"✅ Bot connected as {bot.user}")
        print(f"✅ Connected to {len(bot.guilds)} guilds")
        
        for guild in bot.guilds:
            print(f"📋 Guild: {guild.name} (ID: {guild.id})")
            
            # Check bot permissions
            bot_member = guild.get_member(bot.user.id)
            if bot_member:
                permissions = bot_member.guild_permissions
                print(f"🔐 Bot permissions in {guild.name}:")
                print(f"  - Send Messages: {permissions.send_messages}")
                print(f"  - Embed Links: {permissions.embed_links}")
                print(f"  - Read Message History: {permissions.read_message_history}")
                print(f"  - Use Slash Commands: {permissions.use_slash_commands}")
                
                if not permissions.send_messages:
                    print("❌ Bot cannot send messages!")
                if not permissions.embed_links:
                    print("❌ Bot cannot embed links!")
                if not permissions.read_message_history:
                    print("❌ Bot cannot read message history!")
                if not permissions.use_slash_commands:
                    print("❌ Bot cannot use slash commands!")
            else:
                print("❌ Bot member not found in guild!")
        
        # Check slash commands
        try:
            synced = await bot.tree.sync()
            print(f"✅ Synced {len(synced)} slash commands:")
            for cmd in synced:
                print(f"  - /{cmd.name}: {cmd.description}")
        except Exception as e:
            print(f"❌ Failed to sync commands: {e}")
        
        print("\n🔍 Diagnosis complete. Check the permissions above.")
        await bot.close()
    
    try:
        await bot.start(token)
    except discord.LoginFailure:
        print("❌ Invalid bot token!")
    except Exception as e:
        print(f"❌ Bot connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(diagnose_bot())
