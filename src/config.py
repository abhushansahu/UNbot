"""Configuration settings for UN Discord Bot"""
import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv('DISCORD_TOKEN')
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'

# Data Paths
DATA_DIR = 'data'
CHARTER_FILE = f'{DATA_DIR}/un_charter.json'
POLICY_FILE = f'{DATA_DIR}/policy_definitions.json'

# Rate Limiting (seconds)
RATE_LIMITS = {
    'charter': 5,
    'resolution': 3,
    'policy': 3,
    'search': 2,
    'latest': 10,
    'help': 1
}

# Discord Limits
EMBED_TITLE_LIMIT = 256
EMBED_DESC_LIMIT = 4096
EMBED_FIELD_LIMIT = 1024
EMBED_FIELDS_LIMIT = 25

# Colors
COLORS = {
    'success': 0x1f8b4c,
    'warning': 0xffa500,
    'error': 0xe74c3c,
    'info': 0x3498db
}
