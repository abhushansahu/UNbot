#!/bin/bash
# Security check script for UN Discord Bot
# Run this before committing to ensure no sensitive data is included

echo "🔍 Running security checks..."

# Check for .env files
if [ -f .env ]; then
    echo "❌ .env file detected! Remove it before committing."
    exit 1
fi

# Check for hardcoded tokens (excluding documentation and example files)
if grep -r "DISCORD_TOKEN=" . --exclude-dir=.git --exclude-dir=scripts --exclude="env_example.txt" --exclude=".env.example" --exclude="*.md" --exclude=".pre-commit-config.yaml" 2>/dev/null; then
    echo "❌ Hardcoded DISCORD_TOKEN detected!"
    exit 1
fi

# Check for log files
if find . -name "*.log" -not -path "./.git/*" | grep -q .; then
    echo "❌ Log files detected! Add them to .gitignore."
    exit 1
fi

# Check for sensitive patterns (excluding documentation)
if grep -r -i "password\|secret\|key\|token" . --exclude-dir=.git --exclude-dir=scripts --exclude="env_example.txt" --exclude=".env.example" --exclude="*.md" --exclude=".pre-commit-config.yaml" 2>/dev/null; then
    echo "⚠️  Potential sensitive data detected. Review before committing."
fi

echo "✅ Security checks passed!"
exit 0
