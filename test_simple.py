#!/usr/bin/env python3
"""Simple test for UN Discord Bot"""
import json
import os

def test_data_files():
    """Test that data files exist and are valid JSON"""
    data_files = [
        'data/un_charter.json',
        'data/policy_definitions.json'
    ]
    
    for file_path in data_files:
        if not os.path.exists(file_path):
            print(f"❌ Data file not found: {file_path}")
            return False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"✅ {file_path}: {len(data)} items")
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in {file_path}: {e}")
            return False
    
    return True

def test_imports():
    """Test that all modules can be imported"""
    try:
        from src.config import BOT_TOKEN, DEBUG
        from src.data_manager import DataManager
        from src.rate_limiter import RateLimiter
        from src.utils import sanitize_input, create_embed
        from src.commands import UNBotCommands
        print("✅ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    """Run simple tests"""
    print("🧪 Running simple tests...")
    
    tests = [
        ("Data Files", test_data_files),
        ("Module Imports", test_imports)
    ]
    
    all_passed = True
    for test_name, test_func in tests:
        print(f"\n📋 Testing {test_name}...")
        if not test_func():
            all_passed = False
    
    print("\n" + "="*40)
    if all_passed:
        print("🎉 All tests passed!")
        print("✅ Bot is ready to run")
    else:
        print("❌ Some tests failed!")
        print("⚠️  Please fix the issues before running the bot")

if __name__ == "__main__":
    main()
