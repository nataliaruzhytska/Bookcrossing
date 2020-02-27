from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus
from django.contrib.auth.models import User, Permission

from .forms import UserForm, LibraryForm, BookForm
from .models import Library, Book, WishList
from ..settings import FIXTURES


class ModelsTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        # Создание пользователя
        test_user = User.objects.create_user(username='testuser1', password='12345')
        test_user.save()
        permission1 = Permission.objects.get(codename='add_library')
        permission2 = Permission.objects.get(codename='add_book')
        permission3 = Permission.objects.get(codename='add_wishlist')
        test_user.user_permissions.add(permission1, permission2, permission3)
        test_user.save()
        login = self.client.login(username='testuser1', password='12345')

    def test_library(self):
        obj_count = Library.objects.all().count()
        user = User.objects.get(username='testuser1')
        lib = Library(name='classic', user=user)
        lib.save()
        new_obj_count = Library.objects.all().count()
        self.assertEqual(new_obj_count, obj_count + 1)
        self.assertEqual(Library.objects.get(user=user).name, 'classic')

    def test_book(self):
        obj_count = Book.objects.all().count()
        user = User.objects.get(username='user1')
        lib = Library.objects.get(name='My library1')
        book = Book(name='Book_1', author='Author_1', edition='1st', year_ed='2000',
                    translator='-', lib=lib, user=user)
        print(book.name)
        book.save()
        print(book.name)
        new_obj_count = Book.objects.all().count()
        self.assertEqual(new_obj_count, obj_count + 1)
        self.assertEqual(Book.objects.get(name='Book_1').author, 'Author_1')

    def test_wishlist(self):
        obj_count = WishList.objects.all().count()
        user = User.objects.get(username='testuser1')
        book = Book.objects.get(name='book_001')
        wish_list = WishList(user=user, book=book)
        wish_list.save()
        new_obj_count = WishList.objects.all().count()
        self.assertEqual(new_obj_count, obj_count + 1)
        self.assertEqual(WishList.objects.get(user=user.id).book.id, book.id)


class ViewTests(TestCase):

    def test_health_check(self):
        response = self.client.get(reverse('health_check'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_created_view(self):
        response = self.client.get(reverse('created'))
        self.assertEqual(response.status_code, HTTPStatus.OK)


class BookcrossingViewTests(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        # Создание пользователя
        test_user = User.objects.create_user(username='testuser1', password='12345')
        test_user.save()
        permission1 = Permission.objects.get(codename='view_library')
        permission2 = Permission.objects.get(codename='view_book')
        permission3 = Permission.objects.get(codename='view_wishlist')
        test_user.user_permissions.add(permission1, permission2, permission3)
        test_user.save()
        login = self.client.login(username='testuser1', password='12345')

    def test_book_detail_view(self):
        response = self.client.get(reverse('book_detail', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_lib_detail_view(self):
        response = self.client.get(reverse('library_detail', kwargs={'pk': 5}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_user_detail_view(self):
        response = self.client.get(reverse('user_detail', kwargs={"pk": 3}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_user_list_view(self):
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)

    def test_book_list_view(self):
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)

    def test_lib_list_view(self):
        response = self.client.get(reverse('library_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)

    def test_wish_list_view(self):
        response = self.client.get(reverse('wish_list'))
        self.assertEqual(response.status_code, 200)


class FormTests(TestCase):
    fixtures = FIXTURES

    def test_user_form_valid(self):
        form = UserForm(data={'username': 'user4', 'first_name': 'AAA', 'last_name': 'BBB',
                              'email': 'qqq@gmail.com', 'password': '1234567'})
        self.assertTrue(form.is_valid())

    def test_user_form_invalid(self):
        form = UserForm(data={'username': 'user4', 'first_name': 'AAA', 'last_name': 'BBB',
                              'email': 'qqq@gmail.com', 'password': None})
        self.assertFalse(form.is_valid())

    def test_lib_form_valid(self):
        form = LibraryForm(data={'user': 'user4', 'name': 'my_lib'})
        self.assertTrue(form.is_valid())

    def _test_lib_form_invalid(self):
        form = LibraryForm(data={'user': 'user4', 'name': None})
        self.assertFalse(form.is_valid())

    def test_book_form_valid(self):
        form = BookForm(data={'name': 'book_005', 'author': 'author_005', 'edition': '1st',
                              'year_ed': 2020, 'translator': 't1',
                              'is_visible': True, 'library': 4})
        self.assertTrue(form.is_valid())

    def test_book_form_invalid(self):
        form = BookForm(data={'name': 'book', 'author': None, 'edition': '1st',
                              'year_ed': 2020, 'translator': '-',
                              'is_visible': True, 'library': 4})
        self.assertFalse(form.is_valid())
