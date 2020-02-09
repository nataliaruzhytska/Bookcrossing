from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import health_check, index, created, LibraryView, UserView, BookView, BookListView, UserListView, \
    LibraryListView, LibraryDetailView, UserDetailView, BookDetailView, BookLibList, BookUserList, ContactView, \
    hide_books, show_books, hide_all_books, show_all_books, add_to_wish_list, show_wish_list

urlpatterns = [
    path('healthcheck/', health_check, name='health_check'),
    path('', index, name='index'),
    path('created/', created, name='created'),
    path('<slug:slug>/add_library/', LibraryView.as_view(), name='add_library'),
    path('wish_list/', show_wish_list, name='wish_list'),
    path('<slug:slug>/signin/', UserView.as_view(), name='signin'),
    path('books/', BookListView.as_view(), name='book_list'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('libraries/', LibraryListView.as_view(), name='library_list'),
    path('libraries/library_detail/<pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('libraries/library_detail/<pk>/books/', BookLibList.as_view(), name='lib_books'),
    path('users/user_detail/<pk>/', login_required(UserDetailView.as_view()), name='user_detail'),
    path('users/user_detail/<pk>/books/', login_required(BookUserList.as_view()), name='user_books'),
    path('books/book_detail/<pk>/', login_required(BookDetailView.as_view()), name='user_detail'),
    path('books/book_detail/<pk>/hide_books/', hide_books, name='hide_books'),
    path('users/user_detail/<pk>/hide_all_books/', hide_all_books, name='hide_all_books'),
    path('books/book_detail/<pk>/show_books/', show_books, name='show_books'),
    path('users/user_detail/<pk>/show_all_books/', show_all_books, name='show_all_books'),
    path('books/book_detail/<pk>/send_email/', ContactView.as_view(), name='send_email'),
    path('users/user_detail/<pk>/add_book/', BookView.as_view(), name='add_book'),
    path('books/hide_all_books/', hide_all_books, name='hide_all_books'),
    path('books/show_all_books/', show_all_books, name='show_all_books'),
    path('books/book_detail/<pk>/add_to_wish_list/', add_to_wish_list, name='add_to_wish_list'),
]
