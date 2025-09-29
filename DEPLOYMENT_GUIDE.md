# UN Discord Bot - Deployment Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Discord Bot Token
- Discord Server with appropriate permissions

### 1. Install Dependencies
```bash
pip3 install -r requirements.txt
```

### 2. Configure Environment
1. Copy `env_example.txt` to `.env`
2. Add your Discord bot token:
```bash
DISCORD_TOKEN=your_discord_bot_token_here
DEBUG=false
```

### 3. Test the Bot
```bash
python3 test_comprehensive.py
```

### 4. Run the Bot
```bash
python3 bot.py
```

## 🔧 Bot Setup in Discord

### 1. Create Discord Application
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Give it a name (e.g., "UN Bot")
4. Go to "Bot" section
5. Click "Add Bot"
6. Copy the bot token and add it to your `.env` file

### 2. Configure Bot Permissions
Required permissions:
- Send Messages
- Use Slash Commands
- Embed Links
- Read Message History

### 3. Invite Bot to Server
1. Go to OAuth2 > URL Generator
2. Select scopes: `bot`, `applications.commands`
3. Select permissions: `Send Messages`, `Use Slash Commands`, `Embed Links`
4. Copy the generated URL and open it in your browser
5. Select your server and authorize

## 📋 Available Commands

### Slash Commands
- `/charter article:51` - Get UN Charter Article 51
- `/resolution type:sc number:2707` - Search for UN resolutions
- `/policy term:r2p` - Get UN policy definitions
- `/search query:peace` - Search UN Charter and policies
- `/latest` - Get latest UN news and updates
- `/help` - Show all available commands

### Command Examples
```
/charter article:51
/resolution type:sc number:2707
/policy term:r2p
/search query:peace
/latest
/help
```

## 🌐 UN Website Integration

The bot can extract real-time data from:
- **UN News** (https://news.un.org/)
- **UN Press Releases** (https://press.un.org/)
- **Security Council** (https://www.un.org/securitycouncil/)
- **UN Digital Library** (https://digitallibrary.un.org/)
- **UN Charter** (https://www.un.org/en/about-us/un-charter)

## 🔍 Data Sources

### Local Data (Fast)
- UN Charter articles (8 articles)
- Policy definitions (8 terms)
- Stored in `data/` directory

### Online Data (Real-time)
- Latest UN news
- Security Council updates
- Resolution searches
- Policy definitions from UN websites

## 🛠️ Troubleshooting

### Common Issues

#### 1. Bot Not Responding to Slash Commands
- **Solution**: Wait 1-2 minutes for command sync
- **Check**: Bot has `applications.commands` scope
- **Verify**: Bot is online and has proper permissions

#### 2. "Interaction Failed" Errors
- **Check**: Bot has "Use Slash Commands" permission
- **Verify**: Bot is in the server where commands are used
- **Solution**: Re-invite bot with correct permissions

#### 3. Rate Limiting
- **Info**: Bot has built-in rate limiting (1-10 seconds per command)
- **Solution**: Wait for cooldown period to expire

#### 4. Data Not Found
- **Charter**: Only articles 1, 2, 51, 55, 56, 73, 99, 100 are available locally
- **Policy**: Only R2P, SDGs, UNSC, UNGA, Peacekeeping, etc. are available
- **Solution**: Use `/search` to find available content

### Debug Mode
Set `DEBUG=true` in `.env` file for detailed logging.

## 📊 Monitoring

### Logs
- Bot logs are saved to `bot.log`
- Console output shows real-time status
- Error handling for all commands

### Health Checks
```bash
# Test data integrity
python3 test_simple.py

# Comprehensive test
python3 test_comprehensive.py

# Test UN scraper
python3 -c "import asyncio; from src.un_scraper import test_un_scraper; asyncio.run(test_un_scraper())"
```

## 🔒 Security Features

- Input sanitization
- Rate limiting per user
- Error handling
- No sensitive data storage
- Respectful web scraping

## 📈 Performance

- **Local Data**: Instant response (< 100ms)
- **Online Data**: 1-3 seconds (depends on UN website)
- **Rate Limits**: 1-10 seconds per command per user
- **Memory Usage**: < 50MB

## 🆘 Support

If you encounter issues:
1. Check the logs in `bot.log`
2. Run the test suite: `python3 test_comprehensive.py`
3. Verify your Discord bot token is correct
4. Ensure bot has proper permissions in your server

## 🎯 Features Summary

✅ **Slash Commands** - Modern Discord command interface  
✅ **UN Charter Access** - Full text of key articles  
✅ **Policy Definitions** - UN terminology and concepts  
✅ **Real-time News** - Latest UN updates  
✅ **Resolution Search** - Security Council and GA resolutions  
✅ **Rate Limiting** - Prevents spam and abuse  
✅ **Error Handling** - Graceful error management  
✅ **UN Website Integration** - Live data from official sources  
✅ **Comprehensive Testing** - Full test suite included  
✅ **Security** - Input sanitization and validation  

The bot is ready for production use! 🚀