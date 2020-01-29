from django import forms
from .models import User, Book, Library


class UserForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.CharField()

    def save_user(self):
        user = User(first_name=self.data['first_name'], last_name=self.data['last_name'], email=self.data['email'])
        user.save()


class BookForm(forms.Form):
    name = forms.CharField()
    author = forms.CharField()
    edition = forms.CharField()
    year_ed = forms.IntegerField()
    translator = forms.CharField()
    is_visible = forms.BooleanField()

    def save_book(self, pk):
        user = User.objects.get(id=pk)
        library = Library.objects.get(user=user)
        book = Book(name=self.data['name'], author=self.data['author'], edition=self.data.get('edition'),
                    year_ed=int(self.data.get('year_ed')), translator=self.data.get('translator'),
                    lib=library, user=user)
        book.save()


class LibraryForm(forms.Form):
    name = forms.CharField()
    user = forms.IntegerField()

    def save_library(self):
        user = User.objects.get(id=int(self.data['user']))
        library = Library(name=self.data['name'], user=user)
        library.save()
