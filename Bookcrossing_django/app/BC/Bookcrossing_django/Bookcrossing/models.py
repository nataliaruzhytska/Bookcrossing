from django.db import models


class User(models.Model):
    first_name = models.CharField(
        'First name',
        max_length=250,
    )
    last_name = models.CharField(
        'Last name',
        max_length=250,
    )
    email = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        db_index=True,
    )

    @property
    def fullname(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.fullname

    class Meta:
        ordering = ['first_name', 'last_name']
        indexes = [
            models.Index(fields=['first_name', 'last_name']),
        ]


class Library(models.Model):
    name = models.CharField(
        'Library name',
        max_length=250,
    )

    user = models.OneToOneField(
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
    year_ed = models.IntegerField(
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
