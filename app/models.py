from django.db import models


class Resume(models.Model):

    ROLE_CHOICES = [

        ('Django Developer', 'Django Developer'),

        ('Frontend Developer', 'Frontend Developer'),

        ('Backend Developer', 'Backend Developer'),

        ('Python Developer', 'Python Developer'),

    ]

    name = models.CharField(
        max_length=100
    )

    role = models.CharField(
        max_length=100,
        choices=ROLE_CHOICES
    )

    score = models.IntegerField(
        default=0
    )

    resume = models.FileField(
        upload_to='resumes/'
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.name