from django.conf import settings
from django.db import models


class Course(models.Model):
    """
    Определение модели курс
    """

    name = models.CharField(max_length=100)
    preview = models.ImageField(upload_to="preview/", blank=True, null=True)
    video_url = models.URLField(max_length=200, verbose_name="Ссылка на видео")
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Владелец",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"
        ordering = ["name"]


class Lesson(models.Model):
    """
    Определение модели урок
    """

    name = models.CharField(max_length=100)
    description = models.TextField()
    preview = models.ImageField(upload_to="preview/", blank=True, null=True)
    video_url = models.URLField(max_length=200, verbose_name="Ссылка на видео")
    course = models.ForeignKey(
        "Course", on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Владелец",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
        ordering = ["created_at"]


class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions"
    )
    course = models.ForeignKey(
        "Course", on_delete=models.CASCADE, related_name="subscribers"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "course")

    def __str__(self):
        return f"{self.user} -> {self.course}"
