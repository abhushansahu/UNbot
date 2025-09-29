"""Rate limiting for Discord bot commands"""
import time
from typing import Dict, Tuple
from .config import RATE_LIMITS

class RateLimiter:
    """Simple rate limiter for bot commands"""
    
    def __init__(self):
        self.user_cooldowns: Dict[int, Dict[str, float]] = {}
    
    def is_rate_limited(self, user_id: int, command: str) -> Tuple[bool, float]:
        """
        Check if user is rate limited for a command
        Returns: (is_limited, remaining_time)
        """
        now = time.time()
        cooldown = RATE_LIMITS.get(command, 5)
        
        if user_id not in self.user_cooldowns:
            self.user_cooldowns[user_id] = {}
        
        if command in self.user_cooldowns[user_id]:
            last_used = self.user_cooldowns[user_id][command]
            remaining = cooldown - (now - last_used)
            
            if remaining > 0:
                return True, remaining
        
        self.user_cooldowns[user_id][command] = now
        return False, 0.0
    
    def get_remaining_time(self, user_id: int, command: str) -> float:
        """Get remaining cooldown time for a command"""
        if user_id not in self.user_cooldowns:
            return 0.0
        
        if command not in self.user_cooldowns[user_id]:
            return 0.0
        
        now = time.time()
        cooldown = RATE_LIMITS.get(command, 5)
        last_used = self.user_cooldowns[user_id][command]
        remaining = cooldown - (now - last_used)
        
        return max(0.0, remaining)
