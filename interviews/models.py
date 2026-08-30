from django.db import models

from applications.models import Application


class Interview(models.Model):
    class Type(models.TextChoices):
        HR = "hr", "HR"
        TECHNICAL = "technical", "Technical"
        FINAL = "final", "Final"

    class Result(models.TextChoices):
        PENDING = "pending", "Pending"
        PASSED = "passed", "Passed"
        FAILED = "failed", "Failed"

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="interviews",
    )
    type = models.CharField(
        max_length=20,
        choices=Type.choices,
    )
    scheduled_at = models.DateTimeField()
    result = models.CharField(
        max_length=10,
        choices=Result.choices,
        default=Result.PENDING,
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("scheduled_at",)
        verbose_name = "Interview"
        verbose_name_plural = "Interviews"

    def __str__(self):
        return f"{self.get_type_display()} interview for {self.application}"
