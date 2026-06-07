import random
import string
from yarl import URL
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

# генерирует цифробуквы
def generate_short_code(length: int = 6) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# проверка схемы и наличие хоста
def is_valid_url(url: str) -> bool:
    url = url.strip()

    # быстрая проверка через ярл
    try:
        parsed = URL(url)
        if not parsed.scheme or not parsed.host:
            return False
        if parsed.scheme not in ('http', 'https'):
            return False
    except Exception:
        return False

    # строгая проверка через джанго урлвалидатор
    validator = URLValidator()
    try:
        validator(url)
        return True
    except ValidationError:
        return False