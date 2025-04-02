
import os
from typing import Dict, Any

class Config:
    SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
    DOMO_ACCESS_TOKEN = os.environ.get("DOMO_ACCESS_TOKEN")
    DOMO_INSTANCE = os.environ.get("DOMO_INSTANCE")
    
    @classmethod
    def get_all(cls) -> Dict[str, Any]:
        return {
            key: value for key, value in cls.__dict__.items() 
            if not key.startswith('_')
        }
