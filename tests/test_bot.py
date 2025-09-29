#!/usr/bin/env python3
"""Comprehensive test suite for UN Discord Bot"""
import json
import os
import sys
import asyncio
from unittest.mock import Mock, AsyncMock
import discord

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_data_integrity():
    """Test data files integrity and content"""
    print("🔍 Testing data integrity...")
    
    # Test charter data
    charter_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'un_charter.json')
    with open(charter_path, 'r', encoding='utf-8') as f:
        charter_data = json.load(f)
    
    print(f"✅ Charter data: {len(charter_data)} articles")
    
    # Test policy data
    policy_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'policy_definitions.json')
    with open(policy_path, 'r', encoding='utf-8') as f:
        policy_data = json.load(f)
    
    print(f"✅ Policy data: {len(policy_data)} terms")
    
    # Test specific content
    test_article = charter_data.get('51')
    if test_article:
        print(f"✅ Article 51: {test_article.get('title', 'No title')}")
    
    test_policy = policy_data.get('r2p')
    if test_policy:
        print(f"✅ R2P Policy: {test_policy.get('title', 'No title')}")
    
    return True

def test_imports():
    """Test all module imports"""
    print("🔍 Testing module imports...")
    
    try:
        from src.config import BOT_TOKEN, DEBUG, COLORS
        from src.data_manager import DataManager
        from src.rate_limiter import RateLimiter
        from src.utils import sanitize_input, create_embed, validate_article_number
        from src.commands import UNBotCommands
        print("✅ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_data_manager():
    """Test DataManager functionality"""
    print("🔍 Testing DataManager...")
    
    try:
        from src.data_manager import DataManager
        dm = DataManager()
        
        # Test charter article retrieval
        article = dm.get_charter_article(51)
        if article:
            print(f"✅ Charter article 51: {article.get('title', 'No title')}")
        else:
            print("❌ Charter article 51 not found")
            return False
        
        # Test policy term retrieval
        policy = dm.get_policy_term('r2p')
        if policy:
            print(f"✅ Policy term R2P: {policy.get('title', 'No title')}")
        else:
            print("❌ Policy term R2P not found")
            return False
        
        # Test search functionality
        charter_results = dm.search_charter('peace')
        print(f"✅ Charter search results: {len(charter_results)}")
        
        policy_results = dm.search_policy('protection')
        print(f"✅ Policy search results: {len(policy_results)}")
        
        return True
    except Exception as e:
        print(f"❌ DataManager error: {e}")
        return False

def test_utils():
    """Test utility functions"""
    print("🔍 Testing utility functions...")
    
    try:
        from src.utils import sanitize_input, validate_article_number, create_embed
        
        # Test sanitize_input
        test_input = "Test <@123456789> input"
        sanitized = sanitize_input(test_input)
        if sanitized == "Test 123456789 input":
            print("✅ Input sanitization works")
        else:
            print(f"❌ Input sanitization failed: expected 'Test 123456789 input', got '{sanitized}'")
            return False
        
        # Test validation functions
        if validate_article_number(51) and not validate_article_number(1000):
            print("✅ Article number validation works")
        else:
            print("❌ Article number validation failed")
            return False
        
        # Test embed creation
        embed = create_embed("Test Title", "Test Description")
        if embed.title == "Test Title" and embed.description == "Test Description":
            print("✅ Embed creation works")
        else:
            print("❌ Embed creation failed")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Utils error: {e}")
        return False

async def test_commands():
    """Test command handlers with mocked interactions"""
    print("🔍 Testing command handlers...")
    
    try:
        from src.data_manager import DataManager
        from src.rate_limiter import RateLimiter
        from src.commands import UNBotCommands
        
        # Create mock components
        dm = DataManager()
        rl = RateLimiter()
        commands = UNBotCommands(dm, rl)
        
        # Create mock interaction
        mock_interaction = Mock()
        mock_interaction.user = Mock()
        mock_interaction.user.id = 123456789
        mock_interaction.user.name = "TestUser"
        mock_interaction.response = AsyncMock()
        
        # Test charter command
        await commands.charter(mock_interaction, 51)
        print("✅ Charter command test passed")
        
        # Test policy command
        await commands.policy(mock_interaction, "r2p")
        print("✅ Policy command test passed")
        
        # Test search command
        await commands.search(mock_interaction, "peace")
        print("✅ Search command test passed")
        
        # Test latest command
        await commands.latest(mock_interaction)
        print("✅ Latest command test passed")
        
        # Test help command
        await commands.help_command(mock_interaction)
        print("✅ Help command test passed")
        
        return True
    except Exception as e:
        print(f"❌ Commands test error: {e}")
        return False

def test_environment():
    """Test environment configuration"""
    print("🔍 Testing environment configuration...")
    
    try:
        from src.config import BOT_TOKEN, DEBUG
        
        if BOT_TOKEN:
            print("✅ Discord token found")
        else:
            print("⚠️  Discord token not found - bot won't start without it")
        
        print(f"✅ Debug mode: {DEBUG}")
        return True
    except Exception as e:
        print(f"❌ Environment test error: {e}")
        return False

def test_bot_imports():
    """Test that bot can be imported without errors"""
    print("🔍 Testing bot imports...")
    
    try:
        # Test main bot import
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        from bot import bot, main
        print("✅ Main bot module imported successfully")
        
        # Test all command imports
        from src.commands import UNBotCommands
        from src.data_manager import DataManager
        from src.rate_limiter import RateLimiter
        from src.config import BOT_TOKEN, DEBUG
        print("✅ All bot components imported successfully")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_bot_initialization():
    """Test bot initialization without running"""
    print("🔍 Testing bot initialization...")
    
    try:
        from src.data_manager import DataManager
        from src.rate_limiter import RateLimiter
        from src.commands import UNBotCommands
        
        # Initialize components
        dm = DataManager()
        rl = RateLimiter()
        commands = UNBotCommands(dm, rl)
        
        print("✅ Bot components initialized successfully")
        print(f"✅ Data manager loaded: {len(dm.charter_data)} charter articles, {len(dm.policy_data)} policy terms")
        
        return True
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        return False

def test_slash_commands():
    """Test slash command definitions"""
    print("🔍 Testing slash command definitions...")
    
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        from bot import bot
        
        # Check if bot has command tree
        if hasattr(bot, 'tree'):
            print("✅ Bot has command tree")
        else:
            print("❌ Bot missing command tree")
            return False
        
        # Check if commands are registered
        commands = bot.tree.get_commands()
        print(f"✅ Found {len(commands)} slash commands:")
        for cmd in commands:
            print(f"  - /{cmd.name}: {cmd.description}")
        
        return True
    except Exception as e:
        print(f"❌ Slash commands error: {e}")
        return False

async def test_un_scraper():
    """Test UN scraper functionality"""
    print("🔍 Testing UN scraper...")
    
    try:
        from src.un_scraper import UNScraper
        
        async with UNScraper() as scraper:
            # Test basic functionality
            news = await scraper.get_latest_news(1)
            print(f"✅ UN scraper working: {len(news)} news items found")
            
            if news:
                print(f"  - Latest: {news[0]['title'][:50]}...")
        
        return True
    except Exception as e:
        print(f"❌ UN scraper error: {e}")
        return False

async def main():
    """Run comprehensive tests"""
    print("🧪 Running comprehensive UN Bot tests...")
    print("=" * 50)
    
    tests = [
        ("Environment", test_environment),
        ("Data Integrity", test_data_integrity),
        ("Module Imports", test_imports),
        ("Bot Imports", test_bot_imports),
        ("Bot Initialization", test_bot_initialization),
        ("Data Manager", test_data_manager),
        ("Utility Functions", test_utils),
        ("Slash Commands", test_slash_commands),
        ("Command Handlers", test_commands),
        ("UN Scraper", test_un_scraper)
    ]
    
    all_passed = True
    for test_name, test_func in tests:
        print(f"\n📋 Testing {test_name}...")
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            
            if not result:
                all_passed = False
        except Exception as e:
            print(f"❌ Test {test_name} failed with exception: {e}")
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed!")
        print("✅ Bot is ready to run")
        print("\n📋 Next steps:")
        print("1. Make sure your .env file has a valid DISCORD_TOKEN")
        print("2. Run: python3 bot.py")
        print("3. Invite the bot to your Discord server")
        print("4. Use slash commands like /charter, /policy, /search")
    else:
        print("❌ Some tests failed!")
        print("⚠️  Please fix the issues before running the bot")

if __name__ == "__main__":
    asyncio.run(main())
