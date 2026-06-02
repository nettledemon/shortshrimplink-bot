from django.db import models
from django.utils import timezone


class Link(models.Model):
    # 6 символов для короткой ссылки
    short_code = models.CharField(max_length=10, unique=True, db_index=True)

    # длинная ссылка
    long_url = models.URLField(max_length=2000)

    # дата создания (авто)
    created_at = models.DateTimeField(auto_now_add=True)

    # что показывать в админке и логах
    def __str__(self):
        return f"[{self.created_at}] {self.short_code} -> {self.long_url}"

    # норм формат даты
    def local_created_at(self):
        return timezone.localtime(self.created_at).strftime("%d.%m.%Y %H:%M:%S")