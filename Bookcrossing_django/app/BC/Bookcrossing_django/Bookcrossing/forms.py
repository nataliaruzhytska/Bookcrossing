from django import forms
from django.contrib.auth.models import User

from .models import Book, Library


class UserForm(forms.Form):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.CharField()
    password = forms.CharField()

    def save_user(self):
        user = User(username=self.data['username'], first_name=self.data['first_name'], last_name=self.data['last_name'],
                    email=self.data['email'], password=self.data['password'])
        user.save()


class BookForm(forms.Form):
    name = forms.CharField()
    author = forms.CharField()
    edition = forms.CharField(required=False)
    year_ed = forms.IntegerField(required=False)
    translator = forms.CharField(required=False)
    is_visible = forms.BooleanField(required=False)
    library = forms.CharField()

    def save_book(self, pk):
        user = User.objects.get(id=pk)
        library = Library.objects.get(name=self.data.get('library'))
        book = Book(name=self.data['name'], author=self.data['author'], edition=self.data.get('edition'),
                    year_ed=self.data.get('year_ed'), translator=self.data.get('translator'),
                    is_visible=bool(self.data.get('is_visible')), lib=library, user=user)
        book.save()


class LibraryForm(forms.Form):
    name = forms.CharField()
    user = forms.CharField()

    def save_library(self):
        user = User.objects.get(username=self.data['user'])
        library = Library(name=self.data['name'], user=user)
        library.save()
