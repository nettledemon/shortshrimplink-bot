import random
import string
from yarl import URL

# генерирует цифробуквы
def generate_short_code(length: int = 6) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# проверка схемы и наличие хоста
def is_valid_url(url: str) -> bool:
    url = url.strip()

    try:
        parsed = URL(url)
        return parsed.scheme in ('http', 'https') and bool(parsed.host)
    except ValueError:
        # если url вообще не распарсился
        return False