#!/usr/bin/env python3
"""Generate Discord bot invite URL with proper permissions"""
import os
from dotenv import load_dotenv

load_dotenv()

# Get bot token to extract application ID
bot_token = os.getenv('DISCORD_TOKEN')
if not bot_token:
    print("❌ DISCORD_TOKEN not found in .env file")
    exit(1)

# Extract application ID from token (first part before the dot)
app_id = bot_token.split('.')[0]

# Required permissions for slash commands
permissions = [
    "Send Messages",           # 2048
    "Use Slash Commands",      # 0 (this is a scope, not permission)
    "Embed Links",            # 16384
    "Read Message History",   # 65536
    "Add Reactions"           # 64
]

# Calculate permission integer
permission_int = 2048 + 16384 + 65536 + 64  # Send Messages + Embed Links + Read Message History + Add Reactions

print("🤖 Discord Bot Invite URL Generator")
print("=" * 50)
print(f"Application ID: {app_id}")
print(f"Required Permissions: {', '.join(permissions)}")
print(f"Permission Integer: {permission_int}")
print()

# Generate invite URL
invite_url = f"https://discord.com/api/oauth2/authorize?client_id={app_id}&permissions={permission_int}&scope=bot%20applications.commands"

print("🔗 Bot Invite URL:")
print(invite_url)
print()
print("📋 Instructions:")
print("1. Copy the URL above")
print("2. Open it in your browser")
print("3. Select your Discord server")
print("4. Click 'Authorize'")
print("5. Make sure the bot has the required permissions")
print()
print("⚠️  Important:")
print("- The bot needs 'applications.commands' scope for slash commands")
print("- The bot needs 'Send Messages' permission to respond")
print("- Slash commands may take 1-2 minutes to appear after inviting")
