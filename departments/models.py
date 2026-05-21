from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower


class Department(models.Model):
    name = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(1),
            MaxLengthValidator(200),
        ],
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

        constraints = [
            UniqueConstraint(
                Lower('name'),
                'parent',
                name='unique_department_name_per_parent',
            ),
        ]

    def save(self, *args, **kwargs):
        self.name = self.name.strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Employee(models.Model):
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='employees',
    )

    full_name = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(1),
            MaxLengthValidator(200),
        ],
    )

    position = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(1),
            MaxLengthValidator(200),
        ],
    )

    hired_at = models.DateField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['full_name']

    def save(self, *args, **kwargs):
        self.full_name = self.full_name.strip()
        self.position = self.position.strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name
