import os
import shutil
from pathlib import Path

def ensure_dir(path):
    """Создает директорию, если она не существует"""
    if not os.path.exists(path):
        os.makedirs(path)

def create_file(path, content):
    """Создает файл с указанным содержимым"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def setup_project():
    # Базовая структура проекта
    dirs = [
        'app',
        'app/api',
        'app/api/v1',
        'app/api/v1/endpoints',
        'app/core',
        'app/crud',
        'app/db',
        'app/models',
        'app/schemas',
        'app/email-templates/build'
    ]
    
    # Создаем директории
    for dir_path in dirs:
        ensure_dir(dir_path)

    # Содержимое файлов
    files = {
        'app/utils.py': '''from datetime import datetime, timedelta
from typing import Optional
from pathlib import Path
from jose import jwt
from jinja2 import Template

from app.core.config import settings


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token["sub"]
    except jwt.JWTError:
        return None


def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: dict = None,
) -> None:
    if environment is None:
        environment = {}
    # В будущем здесь будет реализация отправки email
    # Пока просто заглушка
    pass


def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
        template_str = f.read()
    template = Template(template_str)
    server_host = settings.SERVER_HOST
    link = f"{server_host}/reset-password?token={token}"
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template.render(
            project_name=settings.PROJECT_NAME,
            username=email,
            email=email_to,
            valid_hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            link=link,
        ),
    )


def send_new_account_email(email_to: str, username: str, password: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "new_account.html") as f:
        template_str = f.read()
    template = Template(template_str)
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template.render(
            project_name=settings.PROJECT_NAME,
            username=username,
            password=password,
        ),
    )''',

        'app/core/config.py': '''import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # 60 minutes * 24 hours = 24 hours
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 24
    SERVER_NAME: str = "FondsRelations"
    SERVER_HOST: AnyHttpUrl = "http://localhost"
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = "FondsRelations"

    POSTGRES_SERVER: str = "db"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "app"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None
    EMAIL_TEMPLATES_DIR: str = "/app/app/email-templates/build"
    EMAILS_ENABLED: bool = False

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )

    USERS_OPEN_REGISTRATION: bool = True

    FIRST_SUPERUSER: EmailStr = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "admin"

    class Config:
        case_sensitive = True


settings = Settings()''',

        'app/email-templates/build/reset_password.html': '''<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Password Recovery</title>
    </head>
    <body>
        <p>Hi {{ username }},</p>
        <p>
            You have requested to reset your password in {{ project_name }}.
        </p>
        <p>
            Please click the link below to reset your password:
        </p>
        <p>
            <a href="{{ link }}">{{ link }}</a>
        </p>
        <p>
            The link will be valid for {{ valid_hours }} hours.
        </p>
        <p>
            If you didn't request a password reset, please ignore this email.
        </p>
        <p>
            Best regards,<br>
            {{ project_name }} team
        </p>
    </body>
</html>''',

        'app/email-templates/build/new_account.html': '''<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width" />
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>{{ project_name }} - New Account</title>
</head>
<body>
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #333;">Welcome to {{ project_name }}!</h1>
        <p>Hi {{ username }},</p>
        <p>Your account has been created successfully. Here are your login credentials:</p>
        <p><strong>Username:</strong> {{ username }}</p>
        <p><strong>Password:</strong> {{ password }}</p>
        <p>Please change your password after your first login for security reasons.</p>
        <p>Best regards,<br>The {{ project_name }} Team</p>
    </div>
</body>
</html>''',

        'requirements.txt': '''fastapi>=0.68.0,<0.69.0
pydantic>=1.8.0,<2.0.0
uvicorn>=0.15.0,<0.16.0
sqlalchemy>=1.4.0,<1.5.0
python-jose[cryptography]>=3.3.0,<3.4.0
passlib[bcrypt]>=1.7.4,<1.8.0
python-multipart>=0.0.5,<0.0.6
emails>=0.6.0,<0.7.0
psycopg2-binary>=2.9.1,<2.10.0
alembic>=1.7.0,<1.8.0
email-validator>=1.1.2,<1.2.0
jinja2>=3.0.0,<3.1.0'''
    }

    # Создаем файлы
    for file_path, content in files.items():
        create_file(file_path, content)

    print("Проект успешно настроен!")

if __name__ == "__main__":
    setup_project() 