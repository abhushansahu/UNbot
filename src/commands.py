"""Command handlers for UN Discord Bot"""
import logging
from typing import Optional
import discord
from discord.ext import commands

from .data_manager import DataManager
from .rate_limiter import RateLimiter
from .utils import (
    sanitize_input, validate_article_number, validate_resolution_type, 
    validate_resolution_number, create_embed, split_content, COLORS
)

logger = logging.getLogger(__name__)

class UNBotCommands:
    """Command handlers for UN Discord Bot"""
    
    def __init__(self, data_manager: DataManager, rate_limiter: RateLimiter):
        self.data = data_manager
        self.rate_limiter = rate_limiter
    
    async def handle_rate_limit(self, ctx, command: str) -> bool:
        """Handle rate limiting for commands"""
        is_limited, remaining = self.rate_limiter.is_rate_limited(ctx.author.id, command)
        if is_limited:
            await ctx.respond(f"⏳ Please wait {remaining:.1f} seconds before using this command again.", ephemeral=True)
            return True
        return False
    
    async def charter(self, ctx, article: int):
        """Retrieve UN Charter article by number"""
        if await self.handle_rate_limit(ctx, 'charter'):
            return
        
        if not validate_article_number(article):
            await ctx.respond("❌ Invalid article number. Please use a number between 1 and 999.", ephemeral=True)
            return
        
        article_data = self.data.get_charter_article(article)
        if not article_data:
            available = self.data.get_available_articles()
            await ctx.respond(
                f"❌ Article {article} not found. Available articles: {', '.join(map(str, available))}",
                ephemeral=True
            )
            return
        
        embed = create_embed(
            title=f"UN Charter Article {article}",
            description=article_data.get('title', 'No title available'),
            color=COLORS['success'],
            url="https://www.un.org/en/about-us/un-charter"
        )
        
        content = article_data.get('content', 'No content available')
        if len(content) > 4096:
            chunks = split_content(content)
            for i, chunk in enumerate(chunks):
                if i == 0:
                    embed.add_field(name="Content", value=chunk, inline=False)
                else:
                    embed.add_field(name=f"Content (continued {i+1})", value=chunk, inline=False)
        else:
            embed.add_field(name="Content", value=content, inline=False)
        
        embed.set_footer(text="United Nations Charter • Use /help for more commands")
        await ctx.respond(embed=embed)
        logger.info(f"Charter article {article} requested by {ctx.author.name}")
    
    async def resolution(self, ctx, resolution_type: str, number: int):
        """Search for UN resolutions"""
        if await self.handle_rate_limit(ctx, 'resolution'):
            return
        
        if not validate_resolution_type(resolution_type):
            await ctx.respond("❌ Invalid resolution type. Use 'sc' for Security Council or 'ga' for General Assembly.", ephemeral=True)
            return
        
        if not validate_resolution_number(number):
            await ctx.respond("❌ Invalid resolution number. Please use a number between 1 and 9999.", ephemeral=True)
            return
        
        if resolution_type.lower() == 'sc':
            title = f"UN Security Council Resolution {number}"
            un_url = f"https://www.un.org/securitycouncil/content/resolutions-{number}"
        else:
            title = f"UN General Assembly Resolution {number}"
            un_url = f"https://www.un.org/en/ga/{number}"
        
        embed = create_embed(
            title=title,
            description=f"Searching for {resolution_type.upper()} resolution {number}",
            color=COLORS['success'],
            url=un_url
        )
        
        embed.add_field(
            name="Official UN Sources",
            value=f"[UN Official Website]({un_url})\n[UN Digital Library](https://digitallibrary.un.org/search?ln=en&p=resolution+{number})\n[UN Documentation](https://www.un.org/en/documents/)",
            inline=False
        )
        
        embed.add_field(
            name="Search Tips",
            value="• Use the UN Digital Library for full text\n• Check UN official documentation\n• Look for related press releases",
            inline=False
        )
        
        embed.set_footer(text="United Nations Official Documentation • Use /help for more commands")
        await ctx.respond(embed=embed)
        logger.info(f"Resolution {resolution_type.upper()} {number} requested by {ctx.author.name}")
    
    async def policy(self, ctx, term: str):
        """Get UN policy definition"""
        if await self.handle_rate_limit(ctx, 'policy'):
            return
        
        term = sanitize_input(term, 50)
        if not term:
            await ctx.respond("❌ Please provide a valid policy term.", ephemeral=True)
            return
        
        policy_info = self.data.get_policy_term(term)
        if not policy_info:
            available = self.data.get_available_terms()
            await ctx.respond(
                f"❌ Policy term '{term}' not found. Available terms: {', '.join(available[:10])}" +
                (f" and {len(available)-10} more..." if len(available) > 10 else ""),
                ephemeral=True
            )
            return
        
        embed = create_embed(
            title=policy_info.get('title', term.title()),
            description=policy_info.get('description', 'No description available'),
            color=COLORS['success']
        )
        
        if 'sources' in policy_info:
            sources_text = "\n".join(policy_info['sources'][:3])
            embed.add_field(name="Sources", value=sources_text, inline=False)
        
        if 'related_terms' in policy_info:
            related_text = ", ".join(policy_info['related_terms'][:5])
            embed.add_field(name="Related Terms", value=related_text, inline=False)
        
        embed.set_footer(text="United Nations Policy Definitions • Use /help for more commands")
        await ctx.respond(embed=embed)
        logger.info(f"Policy term '{term}' requested by {ctx.author.name}")
    
    async def search(self, ctx, query: str):
        """Search for UN Charter articles or policy terms"""
        if await self.handle_rate_limit(ctx, 'search'):
            return
        
        query = sanitize_input(query, 100)
        if not query:
            await ctx.respond("❌ Please provide a valid search query.", ephemeral=True)
            return
        
        charter_results = self.data.search_charter(query)
        policy_results = self.data.search_policy(query)
        all_results = charter_results + policy_results
        
        if not all_results:
            embed = create_embed(
                title="🔍 Search Results",
                description=f"No results found for '{query}'",
                color=COLORS['warning'],
                footer="Try different keywords or check available terms with /help"
            )
            await ctx.respond(embed=embed)
            return
        
        embed = create_embed(
            title=f"🔍 Search Results for '{query}'",
            description=f"Found {len(all_results)} result(s)",
            color=COLORS['success']
        )
        
        for result in all_results[:5]:  # Limit to 5 results
            if result['type'] == 'Charter Article':
                embed.add_field(
                    name=f"📜 {result['type']} {result['number']}: {result['title']}",
                    value=result['preview'],
                    inline=False
                )
            else:
                embed.add_field(
                    name=f"📋 {result['type']}: {result['title']}",
                    value=result['preview'],
                    inline=False
                )
        
        if len(all_results) > 5:
            embed.add_field(
                name="ℹ️ Note",
                value=f"Showing first 5 of {len(all_results)} results. Try more specific search terms.",
                inline=False
            )
        
        embed.set_footer(text="Use /charter, /policy, or /resolution for specific items • Use /help for more commands")
        await ctx.respond(embed=embed)
        logger.info(f"Search query '{query}' by {ctx.author.name} - {len(all_results)} results")
    
    async def latest(self, ctx):
        """Get latest UN news and updates"""
        if await self.handle_rate_limit(ctx, 'latest'):
            return
        
        embed = create_embed(
            title="Latest UN News & Updates",
            description="Access the most recent UN news and Security Council updates",
            color=COLORS['success']
        )
        
        embed.add_field(
            name="Official UN News Sources",
            value="[UN News](https://news.un.org/)\n[UN Press Releases](https://press.un.org/)\n[Security Council Meetings](https://www.un.org/securitycouncil/content/meetings)",
            inline=False
        )
        
        embed.add_field(
            name="Recent Updates",
            value="• Check UN News for latest developments\n• Security Council meeting schedules\n• General Assembly updates\n• Secretary-General statements",
            inline=False
        )
        
        embed.add_field(
            name="Quick Links",
            value="[UN Official Website](https://www.un.org/)\n[UN Digital Library](https://digitallibrary.un.org/)\n[UN Documentation](https://www.un.org/en/documents/)",
            inline=False
        )
        
        embed.set_footer(text="United Nations Official Information • Use /help for more commands")
        await ctx.respond(embed=embed)
        logger.info(f"Latest news requested by {ctx.author.name}")
    
    async def help_command(self, ctx):
        """Show help information"""
        if await self.handle_rate_limit(ctx, 'help'):
            return
        
        embed = create_embed(
            title="🌍 UN Bot Commands",
            description="A Discord bot for UN Charter, resolutions, and policy information",
            color=COLORS['success'],
            fields=[
                {
                    'name': '/charter',
                    'value': "Retrieves full text of a UN Charter Article\nUsage: `/charter article:51`",
                    'inline': False
                },
                {
                    'name': '/resolution',
                    'value': "Searches for Security Council or General Assembly resolutions\nUsage: `/resolution type:sc number:2707`",
                    'inline': False
                },
                {
                    'name': '/policy',
                    'value': "Provides definitions of UN policy terms\nUsage: `/policy term:r2p`",
                    'inline': False
                },
                {
                    'name': '/search',
                    'value': "Search for UN Charter articles or policy terms\nUsage: `/search query:peace`",
                    'inline': False
                },
                {
                    'name': '/latest',
                    'value': "Posts latest UN news and Security Council updates\nUsage: `/latest`",
                    'inline': False
                }
            ],
            footer="Built for informed civic engagement and policy understanding • Rate limits apply"
        )
        await ctx.respond(embed=embed)
        logger.info(f"Help requested by {ctx.author.name}")
