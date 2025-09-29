"""Data management for UN Charter and Policy definitions"""
import json
import logging
from typing import Dict, Any, Optional
from .config import CHARTER_FILE, POLICY_FILE

logger = logging.getLogger(__name__)

class DataManager:
    """Manages UN Charter and Policy data"""
    
    def __init__(self):
        self.charter_data: Dict[str, Any] = {}
        self.policy_data: Dict[str, Any] = {}
        self._load_data()
    
    def _load_data(self) -> None:
        """Load all data files"""
        self.charter_data = self._load_json(CHARTER_FILE)
        self.policy_data = self._load_json(POLICY_FILE)
    
    def _load_json(self, filepath: str) -> Dict[str, Any]:
        """Load JSON data with error handling"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.info(f"Loaded {len(data)} items from {filepath}")
                return data
        except FileNotFoundError:
            logger.error(f"Data file not found: {filepath}")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {filepath}: {e}")
            return {}
        except Exception as e:
            logger.error(f"Error loading {filepath}: {e}")
            return {}
    
    def get_charter_article(self, article_num: int) -> Optional[Dict[str, Any]]:
        """Get charter article by number"""
        return self.charter_data.get(str(article_num))
    
    def get_policy_term(self, term: str) -> Optional[Dict[str, Any]]:
        """Get policy term by name"""
        term_lower = term.lower()
        
        # Direct match
        if term_lower in self.policy_data:
            return self.policy_data[term_lower]
        
        # Search in aliases
        for key, value in self.policy_data.items():
            if term_lower in value.get('aliases', []):
                return value
        
        return None
    
    def search_charter(self, query: str) -> list:
        """Search charter articles"""
        query_lower = query.lower()
        results = []
        
        for article_num, article_data in self.charter_data.items():
            if (query_lower in article_data.get('title', '').lower() or 
                query_lower in article_data.get('content', '').lower()):
                results.append({
                    'type': 'Charter Article',
                    'number': article_num,
                    'title': article_data.get('title', 'No title'),
                    'preview': article_data.get('content', '')[:200] + '...'
                })
        
        return results
    
    def search_policy(self, query: str) -> list:
        """Search policy terms"""
        query_lower = query.lower()
        results = []
        
        for term, term_data in self.policy_data.items():
            if (query_lower in term or 
                query_lower in term_data.get('title', '').lower() or
                query_lower in term_data.get('description', '').lower()):
                results.append({
                    'type': 'Policy Term',
                    'term': term,
                    'title': term_data.get('title', 'No title'),
                    'preview': term_data.get('description', '')[:200] + '...'
                })
        
        return results
    
    def get_available_articles(self) -> list:
        """Get list of available charter articles"""
        return sorted([int(k) for k in self.charter_data.keys()])
    
    def get_available_terms(self) -> list:
        """Get list of available policy terms"""
        return sorted(self.policy_data.keys())
