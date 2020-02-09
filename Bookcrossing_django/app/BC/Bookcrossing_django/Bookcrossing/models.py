from django.db import models
from django.contrib.auth.models import User


class Library(models.Model):
    name = models.CharField(
        'Library name',
        max_length=250,
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )


class Book(models.Model):

    name = models.CharField(
        'Book name',
        max_length=250,
    )
    author = models.CharField(
        'Author',
        max_length=250,
    )
    edition = models.CharField(
        'Edition',
        max_length=250,
        null=True,
        blank=True
    )
    year_ed = models.CharField(
        max_length=250,
        null=True,
        blank=True

    )
    translator = models.CharField(
        max_length=250,
        null=True,
        blank=True,
    )
    lib = models.ForeignKey(
        Library,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    is_visible = models.BooleanField(
        'is_visible',
        default=True
    )

    @property
    def full_info(self):
        return f'{self.name} {self.author}, {self.translator}, {self.edition} {self.year_ed}'

    def short_info(self):
        return f'{self.name} {self.author}'

    def __str__(self):
        return self.full_info

    class Meta:
        ordering = ['name', 'author']
        indexes = [
            models.Index(fields=['name', 'author']),
        ]


class WishList(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE
    )

    @property
    def wish_list(self):
        return f'{self.book.short_info}, {self.book.user.username}'
