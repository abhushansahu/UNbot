# UN Discord Bot

A modular Discord bot for UN Charter articles, resolutions, and policy information.

## Features

- **`/charter`** - Retrieve UN Charter articles
- **`/resolution`** - Search Security Council/General Assembly resolutions  
- **`/policy`** - Get UN policy definitions
- **`/search`** - Search across Charter articles and policy terms
- **`/latest`** - Access recent UN news and updates
- **`/help`** - View all available commands

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup Environment**
   ```bash
   cp env_example.txt .env
   # Edit .env and add your Discord bot token
   # NEVER commit .env files - they contain sensitive tokens!
   ```

3. **Run Bot**
   ```bash
   python bot.py
   ```

## Project Structure

```
UNbot/
├── bot.py                 # Main bot application
├── src/                   # Modular source code
│   ├── __init__.py
│   ├── config.py          # Configuration settings
│   ├── data_manager.py    # Data loading and management
│   ├── rate_limiter.py    # Rate limiting system
│   ├── commands.py        # Command handlers
│   └── utils.py           # Utility functions
├── data/                  # Data files
│   ├── un_charter.json
│   └── policy_definitions.json
├── requirements.txt       # Dependencies
├── env_example.txt        # Environment template
└── README.md             # This file
```

## Configuration

- **DISCORD_TOKEN**: Your Discord bot token
- **DEBUG**: Enable debug mode (true/false)

## Bot Permissions

- Send Messages
- Use Slash Commands
- Embed Links
- Read Message History

## Development

The bot is built with modularity in mind:

- **`src/config.py`**: Centralized configuration
- **`src/data_manager.py`**: Data loading and search functionality
- **`src/rate_limiter.py`**: Rate limiting system
- **`src/commands.py`**: Command handlers
- **`src/utils.py`**: Utility functions

## License

MIT License - Educational and civic engagement use.