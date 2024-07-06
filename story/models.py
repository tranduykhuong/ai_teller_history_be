from django.db import models


class Story(models.Model):
    class Meta:
        db_table = "story"
        verbose_name = "Story"
        verbose_name_plural = "Stories"

    title = models.CharField(max_length=255)
    summary = models.CharField(max_length=500)
    content = models.CharField(max_length=1000000)

    context = models.CharField(max_length=500, default="")
    historical_significance = models.CharField(max_length=500, default="")
    main_happenings = models.CharField(max_length=1000, default="")
    result = models.CharField(max_length=500, default="")

    period = models.CharField(
        null=True,
        blank=True,
        max_length=20
    )

    historical_figures = models.CharField(
        null=True,
        blank=True,
        max_length=255
    )

    created_at = models.DateTimeField(
        verbose_name="Created At",
        auto_now_add=True,
        editable=False,
    )

    def __str__(self):
        return self.title


class GeneratedStory(models.Model):
    class Meta:
        db_table = "generated_story"
        verbose_name = "Generated story"
        verbose_name_plural = "Generated stories"

    story = models.ForeignKey(
        "story.Story",
        related_name="generated_stories",
        verbose_name="Story",
        on_delete=models.CASCADE,
    )

    object = models.CharField(
        null=True,
        blank=True,
        max_length=50
    )

    style = models.CharField(
        null=True,
        blank=True,
        max_length=50
    )

    purpose = models.CharField(
        null=True,
        blank=True,
        max_length=50
    )

    data = models.JSONField(
        null=True,
        blank=True,
    )

    is_publish = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.story} - {self.object} - {self.purpose} - {self.style}'


class StoryImages(models.Model):
    class Meta:
        db_table = "story_images"
        verbose_name = "Story images"
        verbose_name_plural = "Story images"

    story = models.ForeignKey(
        "story.Story",
        related_name="story_imgs",
        verbose_name="Story",
        on_delete=models.CASCADE,
    )

    url = models.CharField(max_length=255)
    description = models.CharField(max_length=255, default="")

    def __str__(self):
        return f'{self.story} - {self.url}'


class SystemSettings(models.Model):
    class Meta:
        db_table = "system_settings"
        verbose_name = "System setting"
        verbose_name_plural = "System settings"

    key = models.CharField(max_length=100)
    value = models.CharField(max_length=500)

    def __str__(self):
        return self.key
