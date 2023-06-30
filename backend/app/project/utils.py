from urllib.parse import urljoin

from .settings import settings


def get_absolute_uri(path: str) -> str:
    return urljoin(settings.domain, path)
