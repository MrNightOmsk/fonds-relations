import logging
from pathlib import Path
from typing import Any, Dict, Optional

import emails
from emails.template import JinjaTemplate
from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.core.config import settings

env = Environment(
    loader=FileSystemLoader(Path(__file__).parent.parent / "templates"),
    autoescape=select_autoescape(['html', 'xml'])
)


def send_email(
    email_to: str,
    subject: str = "",
    template_str: str = "",
    template_data: Dict[str, Any] = {},
) -> None:
    """
    Send an email using a template.
    
    Args:
        email_to: Recipient email address
        subject: Email subject
        template_str: Name of the template file
        template_data: Data to be passed to the template
    """
    assert settings.EMAILS_FROM_EMAIL
    
    # Get the template
    template = env.get_template(template_str)
    html = template.render(**template_data)
    
    # Prepare the email
    message = emails.Message(
        subject=subject,
        html=html,
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    
    # Send the email
    response = message.send(
        to=email_to,
        smtp={
            "host": settings.SMTP_HOST,
            "port": settings.SMTP_PORT,
            "user": settings.SMTP_USER,
            "password": settings.SMTP_PASSWORD,
            "tls": settings.SMTP_TLS,
        },
    )
    
    logging.info(f"Send email result: {response}")


def send_test_email(email_to: str) -> None:
    """Send a test email."""
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test email"
    
    template_data = {"project_name": project_name, "email": email_to}
    
    send_email(
        email_to=email_to,
        subject=subject,
        template_str="test_email.html",
        template_data=template_data,
    )


def send_reset_password_email(email_to: str, token: str) -> None:
    """Send password reset email."""
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Сброс пароля"
    
    template_data = {
        "project_name": project_name,
        "username": email_to,
        "email": email_to,
        "valid_hours": 24,
        "token": token,
    }
    
    send_email(
        email_to=email_to,
        subject=subject,
        template_str="reset_password.html",
        template_data=template_data,
    ) 