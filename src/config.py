import os
import yaml
from pathlib import Path
from typing import Dict, Any


class Config:
    def __init__(self, config_path: str = "config/config.yml"):
        self.config_path = Path(config_path)
        self.data = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f) or {}
        return {}

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split('.')
        value = self.data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

    def get_email_config(self) -> Dict[str, Any]:
        smtp_server = os.getenv('SMTP_SERVER') or self.get('email.smtp_server', 'smtp.gmail.com')
        smtp_port = os.getenv('SMTP_PORT') or self.get('email.smtp_port', 587)
        sender_email = os.getenv('GMAIL_USER') or self.get('email.sender_email')
        sender_password = os.getenv('GMAIL_PASSWORD') or self.get('email.sender_password')
        recipient_email = os.getenv('RECIPIENT_EMAIL') or self.get('email.recipient_email')

        return {
            'smtp_server': smtp_server,
            'smtp_port': int(smtp_port) if smtp_port else 587,
            'sender_email': sender_email,
            'sender_password': sender_password,
            'recipient_email': recipient_email,
        }
