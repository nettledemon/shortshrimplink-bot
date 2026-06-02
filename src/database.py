# джанго орм синхронный, бот асинхронный, поэтому везде sync_to_async
# импорты внутри, чтобы модель запустилась после настройки джанги

from asgiref.sync import sync_to_async


# сохраняет ссылку
@sync_to_async
def save_link(short_code: str, long_url: str):
    from src.models import Link
    link = Link(short_code=short_code, long_url=long_url)
    link.save()
    return link


# забирает длинную ссылку по короткому коду
@sync_to_async
def get_long_url(short_code: str) -> str | None:
    from src.models import Link
    try:
        link = Link.objects.get(short_code=short_code)
        return link.long_url
    except Link.DoesNotExist:
        return None


# проверяет существование короткой ссылки, чтобы не было коллизий
@sync_to_async
def link_exists(short_code: str) -> bool:
    from src.models import Link
    return Link.objects.filter(short_code=short_code).exists()


# проверка на дубликаты по длинной ссылке
@sync_to_async
def get_short_code_by_long_url(long_url: str) -> str | None:
    from src.models import Link
    try:
        link = Link.objects.get(long_url=long_url)
        return link.short_code
    except Link.DoesNotExist:
        return None