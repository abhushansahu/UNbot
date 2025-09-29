"""Utility functions for the UN Discord Bot"""
import re
from typing import Optional, List, Dict, Any
import discord
from .config import EMBED_TITLE_LIMIT, EMBED_DESC_LIMIT, EMBED_FIELD_LIMIT, EMBED_FIELDS_LIMIT, COLORS

def sanitize_input(text: str, max_length: int = 100) -> str:
    """Sanitize user input to prevent abuse"""
    if not text:
        return ""
    
    # Remove potentially harmful characters
    sanitized = re.sub(r'[<>@#&]', '', text)
    sanitized = sanitized.strip()
    
    # Limit length
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized

def validate_article_number(article: int) -> bool:
    """Validate article number is within reasonable range"""
    return 1 <= article <= 999

def validate_resolution_type(resolution_type: str) -> bool:
    """Validate resolution type"""
    return resolution_type.lower() in ['sc', 'ga']

def validate_resolution_number(number: int) -> bool:
    """Validate resolution number"""
    return 1 <= number <= 9999

def create_embed(title: str, description: str, color: int = COLORS['success'], 
                fields: Optional[List[Dict]] = None, footer: Optional[str] = None,
                url: Optional[str] = None) -> discord.Embed:
    """Create a Discord embed with proper validation and limits"""
    
    # Validate title length
    if len(title) > EMBED_TITLE_LIMIT:
        title = title[:EMBED_TITLE_LIMIT-3] + "..."
    
    # Validate description length
    if len(description) > EMBED_DESC_LIMIT:
        description = description[:EMBED_DESC_LIMIT-3] + "..."
    
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
        url=url
    )
    
    if fields:
        for field in fields[:EMBED_FIELDS_LIMIT]:  # Limit to Discord's field limit
            name = field.get('name', '')
            value = field.get('value', '')
            
            # Validate field lengths
            if len(name) > EMBED_TITLE_LIMIT:
                name = name[:EMBED_TITLE_LIMIT-3] + "..."
            if len(value) > EMBED_FIELD_LIMIT:
                value = value[:EMBED_FIELD_LIMIT-3] + "..."
            
            embed.add_field(
                name=name,
                value=value,
                inline=field.get('inline', False)
            )
    
    if footer and len(footer) <= 2048:
        embed.set_footer(text=footer)
    
    return embed

def split_content(content: str, max_length: int = EMBED_DESC_LIMIT) -> List[str]:
    """Split long content into chunks for Discord embeds"""
    if len(content) <= max_length:
        return [content]
    
    chunks = []
    for i in range(0, len(content), max_length):
        chunk = content[i:i+max_length]
        chunks.append(chunk)
    
    return chunks
