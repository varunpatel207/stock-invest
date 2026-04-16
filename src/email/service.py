import logging
import smtplib
from email.mime.text import MIMEText
from pathlib import Path

from src.config import Config

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self, config_path: str = "config/config.yml"):
        self.config = Config(config_path)
        self.email_config = self.config.get_email_config()

    def send_report(self, report_path: str, subject: str = "Portfolio Report") -> bool:
        try:
            if not Path(report_path).exists():
                logger.error(f"Report file not found: {report_path}")
                return False

            smtp_server = self.email_config.get('smtp_server')
            smtp_port = self.email_config.get('smtp_port')
            sender_email = self.email_config.get('sender_email')
            sender_password = self.email_config.get('sender_password')
            recipient_email = self.email_config.get('recipient_email')

            if not all([smtp_server, smtp_port, sender_email, sender_password, recipient_email]):
                logger.error("Missing email configuration")
                return False

            with open(report_path, 'r') as f:
                html_content = f.read()

            message = MIMEText(html_content, 'html')
            message['From'] = sender_email
            message['To'] = recipient_email
            message['Subject'] = subject

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(message)

            logger.info(f"✓ Email sent to {recipient_email}")
            return True

        except Exception as e:
            logger.error(f"✗ Failed to send email: {e}")
            return False
