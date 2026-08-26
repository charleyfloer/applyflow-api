from django.db import models
from django.conf import settings
from vacancies.models import Vacancy


class Application(models.Model):
    class Status(models.TextChoices):
        SAVED = "saved", "Saved"
        APPLIED = "applied", "Applied"
        SCREENING = "screening", "Screening"
        INTERVIEW = "interview", "Interview"
        OFFER = "offer", "Offer"
        REJECTED = "rejected", "Rejected"
        WITHDRAWN = "withdrawn", "Withdrawn"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="applications",
    )
    vacancy = models.ForeignKey(
        Vacancy, 
        on_delete=models.CASCADE, 
        related_name="applications",
    )
    status = models.CharField(
        max_length=20, 
        choices=Status.choices,
        default=Status.SAVED,
    )
    source = models.CharField(max_length=100, blank=True)
    resume = models.FileField(
        upload_to="resumes/",
        blank=True,
    )
    cover_letter = models.FileField(
        upload_to="cover_letters/",
        blank=True,
    )
    notes = models.TextField(blank=True)
    applied_at = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Application"
        verbose_name_plural = "Applications"
        constraints = [
            models.UniqueConstraint(
                fields=("user", "vacancy"),
                name="unique_application_per_user_vacancy",
            ),
        ]

    def __str__(self):
        return f"{self.vacancy.title} ({self.status})"
