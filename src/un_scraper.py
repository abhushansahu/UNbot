"""UN Website Scraper for real-time data extraction"""
import aiohttp
import asyncio
import logging
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
import re
from datetime import datetime

logger = logging.getLogger(__name__)

class UNScraper:
    """Scraper for UN official websites"""
    
    def __init__(self):
        self.session = None
        self.base_urls = {
            'news': 'https://news.un.org/',
            'press': 'https://press.un.org/',
            'security_council': 'https://www.un.org/securitycouncil/',
            'general_assembly': 'https://www.un.org/en/ga/',
            'charter': 'https://www.un.org/en/about-us/un-charter',
            'digital_library': 'https://digitallibrary.un.org/'
        }
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={
                'User-Agent': 'UN-Discord-Bot/1.0 (Educational Purpose)'
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def get_latest_news(self, limit: int = 5) -> List[Dict]:
        """Get latest UN news articles"""
        try:
            async with self.session.get(self.base_urls['news']) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    news_items = []
                    # Look for news article links
                    article_links = soup.find_all('a', href=True)
                    
                    for link in article_links[:limit]:
                        href = link.get('href', '')
                        title = link.get_text(strip=True)
                        
                        if title and len(title) > 10 and 'un.org' in href:
                            news_items.append({
                                'title': title,
                                'url': href if href.startswith('http') else f"https://news.un.org{href}",
                                'source': 'UN News'
                            })
                    
                    return news_items
                else:
                    logger.warning(f"Failed to fetch UN news: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error fetching UN news: {e}")
            return []
    
    async def get_security_council_updates(self) -> List[Dict]:
        """Get latest Security Council updates"""
        try:
            async with self.session.get(self.base_urls['security_council']) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    updates = []
                    # Look for meeting information
                    meeting_links = soup.find_all('a', href=True)
                    
                    for link in meeting_links[:3]:
                        href = link.get('href', '')
                        title = link.get_text(strip=True)
                        
                        if 'meeting' in title.lower() or 'session' in title.lower():
                            updates.append({
                                'title': title,
                                'url': href if href.startswith('http') else f"https://www.un.org{href}",
                                'source': 'Security Council'
                            })
                    
                    return updates
                else:
                    logger.warning(f"Failed to fetch Security Council updates: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error fetching Security Council updates: {e}")
            return []
    
    async def search_resolution(self, resolution_type: str, number: int) -> Optional[Dict]:
        """Search for specific UN resolution"""
        try:
            if resolution_type.lower() == 'sc':
                search_url = f"https://digitallibrary.un.org/search?ln=en&p=resolution+{number}"
            else:
                search_url = f"https://digitallibrary.un.org/search?ln=en&p=resolution+{number}"
            
            async with self.session.get(search_url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Look for resolution links
                    resolution_links = soup.find_all('a', href=True)
                    
                    for link in resolution_links:
                        href = link.get('href', '')
                        title = link.get_text(strip=True)
                        
                        if str(number) in title and ('resolution' in title.lower() or 'res' in title.lower()):
                            return {
                                'title': title,
                                'url': href if href.startswith('http') else f"https://digitallibrary.un.org{href}",
                                'type': resolution_type.upper(),
                                'number': number
                            }
                    
                    return None
                else:
                    logger.warning(f"Failed to search resolution: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Error searching resolution: {e}")
            return None
    
    async def get_charter_article_online(self, article_number: int) -> Optional[Dict]:
        """Get UN Charter article from official website"""
        try:
            async with self.session.get(self.base_urls['charter']) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Look for article content
                    article_pattern = re.compile(rf'article\s*{article_number}', re.IGNORECASE)
                    article_elements = soup.find_all(text=article_pattern)
                    
                    for element in article_elements:
                        parent = element.parent
                        if parent:
                            title = parent.get_text(strip=True)
                            content = parent.get_text(strip=True)
                            
                            if len(content) > 50:  # Ensure substantial content
                                return {
                                    'title': title,
                                    'content': content,
                                    'url': self.base_urls['charter'],
                                    'article_number': article_number
                                }
                    
                    return None
                else:
                    logger.warning(f"Failed to fetch charter article: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Error fetching charter article: {e}")
            return None
    
    async def get_policy_definition_online(self, term: str) -> Optional[Dict]:
        """Search for policy definition on UN websites"""
        try:
            # Search UN documentation
            search_url = f"https://digitallibrary.un.org/search?ln=en&p={term}"
            
            async with self.session.get(search_url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Look for relevant documents
                    doc_links = soup.find_all('a', href=True)
                    
                    for link in doc_links[:3]:
                        href = link.get('href', '')
                        title = link.get_text(strip=True)
                        
                        if term.lower() in title.lower() and len(title) > 10:
                            return {
                                'title': title,
                                'url': href if href.startswith('http') else f"https://digitallibrary.un.org{href}",
                                'term': term,
                                'source': 'UN Digital Library'
                            }
                    
                    return None
                else:
                    logger.warning(f"Failed to search policy definition: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Error searching policy definition: {e}")
            return None

# Example usage function
async def test_un_scraper():
    """Test the UN scraper functionality"""
    print("🔍 Testing UN Website Scraper...")
    
    async with UNScraper() as scraper:
        # Test news scraping
        news = await scraper.get_latest_news(3)
        print(f"✅ Latest news: {len(news)} articles")
        for item in news[:2]:
            print(f"  - {item['title'][:50]}...")
        
        # Test Security Council updates
        sc_updates = await scraper.get_security_council_updates()
        print(f"✅ Security Council updates: {len(sc_updates)} items")
        
        # Test resolution search
        resolution = await scraper.search_resolution('sc', 2707)
        if resolution:
            print(f"✅ Resolution found: {resolution['title']}")
        else:
            print("⚠️  Resolution not found (this is normal for test data)")
        
        # Test charter article
        charter_article = await scraper.get_charter_article_online(51)
        if charter_article:
            print(f"✅ Charter article found: {charter_article['title'][:50]}...")
        else:
            print("⚠️  Charter article not found (this is normal for test data)")
        
        # Test policy definition
        policy = await scraper.get_policy_definition_online('r2p')
        if policy:
            print(f"✅ Policy definition found: {policy['title']}")
        else:
            print("⚠️  Policy definition not found (this is normal for test data)")

if __name__ == "__main__":
    asyncio.run(test_un_scraper())
