import logging
from typing import Optional

from aiosmtplib import SMTP
from ssl import create_default_context
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .base import BaseEmailService
from settings import EMAIL_FROM, EMAIL_HOST, EMAIL_PORT, EMAIL_LOGIN, EMAIL_PASSWORD, EMAIL_TLS

logger = logging.getLogger(__name__)


class SMTPEmailService(BaseEmailService):

    async def send(self, *, message: str, subject: str, to: str, from_who: Optional[str] = None, **kwargs):
        msg = MIMEMultipart('alternative')
        msg['From'] = from_who if from_who is not None else EMAIL_FROM
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'html', 'utf-8'))

        session = SMTP(
            hostname=EMAIL_HOST,
            port=EMAIL_PORT,
            start_tls=EMAIL_TLS,
            tls_context=None if not EMAIL_TLS else create_default_context()
        )

        async with session as connection:
            logger.info('Sending email message')
            logger.debug(f'Message to {msg["To"]} from {msg["From"]} with subject {msg["Subject"]} and text {message}')
            if EMAIL_LOGIN and EMAIL_PASSWORD:
                auth_response = await connection.login(EMAIL_LOGIN, EMAIL_PASSWORD)
                logger.debug(f'Authentication response from smtp server: {auth_response}')
            send_response = await connection.send_message(msg)
            logger.debug(f'Send email response from smtp server: {send_response}')
