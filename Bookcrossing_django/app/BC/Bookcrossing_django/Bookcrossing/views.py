from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import FormView, ListView, DetailView, TemplateView

from .forms import UserForm, BookForm, LibraryForm
from .models import Book, Library,  WishList


def health_check(request):
    return HttpResponse('OK')


def index(request):
    return HttpResponse(render_to_string('index.html', {'title': 'Bookcrossing'}))


def created(request):
    return HttpResponse(render(request, template_name='created.html'))


class UserView(FormView):
    template_name = 'UserForm.html'
    form_class = UserForm
    success_url = '/bookcrossing/created'

    def form_valid(self, form):
        form.save_user()
        return super().form_valid(form)


class BookView(FormView):
    template_name = 'BookForm.html'
    form_class = BookForm
    success_url = '/bookcrossing/created'

    def form_valid(self, form):
        form.save_book(pk=self.kwargs.get('pk'))
        return super().form_valid(form)


class LibraryView(FormView):
    template_name = 'LibraryForm.html'
    form_class = LibraryForm
    success_url = '/bookcrossing/created'

    def form_valid(self, form):
        form.save_library()
        return super().form_valid(form)


class BookListView(ListView):

    model = Book
    queryset = Book.objects.all()
    template_name = 'book_list.html'
    paginate_by = 30

    def get_all_books(self):
        return self.queryset


class BookLibList(BookListView):

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return self.queryset.filter(lib=pk)


class BookUserList(BookListView):
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return self.queryset.filter(user=pk)


class LibraryListView(ListView):

    model = Library
    queryset = Library.objects.all()
    template_name = 'library_list.html'
    paginate_by = 30

    def get_all_libraries(self):
        return self.queryset


class UserListView(ListView):

    model = User
    queryset = User.objects.all()
    template_name = 'user_list.html'
    paginate_by = 30

    def get_all_users(self):
        return self.queryset


class LibraryDetailView(DetailView):

    model = Library()
    queryset = Library.objects.all()
    template_name = 'library_detail.html'

    def get_library(self):
        return self.queryset.filter(library_id=self.kwargs.get('library_id'))


class UserDetailView(DetailView):

    model = User
    queryset = User.objects.all()
    template_name = 'user_detail.html'

    def get_user(self):
        return self.queryset.filter(user_id=self.kwargs.get('user_id'))


class BookDetailView(DetailView):

    model = Book
    queryset = Book.objects.all()
    template_name = 'book_detail.html'

    def get_book(self):
        return self.queryset.filter(book_id=self.kwargs.get('book_id'))


class ContactView(TemplateView):
    template_name = 'email_form.html'

    def post(self, request, *args, **kwargs):
        book = Book.objects.get(user=self.kwargs.get('pk'))
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        from_email = request.POST.get('from_email')
        password = request.POST.get('password')
        send_mail(subject, message, from_email, auth_user=from_email,  auth_password=password, fail_silently=False,
                  recipient_list=[book.user.email])

        return render(request, 'thanks.html')


@login_required
def hide_books(request, pk):
    book = Book.objects.get(id=pk)
    if request.user == book.user:
        book.is_visible = False
        book.save()
        return HttpResponse(render(request, 'successful.html', {'book': book, 'action': ' was hidden'}))
    else:
        return HttpResponse(render(request, "You haven't a permission hide this book"))


@login_required
def hide_all_books(request, pk):
    books = Book.objects.filter(user=pk)
    if request.user == books.first().user:
        for book in books:
            book.is_visible = False
            book.save()
        return HttpResponse(render(request, 'successful.html', {'book': book, 'action': ' was hidden'}))
    else:
        return HttpResponse(render(request, "You haven't a permission hide this book"))

@login_required
def show_books(request, pk):
    book = Book.objects.get(id=pk)
    if request.user == book.user:
        book.is_visible = True
        book.save()
        return HttpResponse(render(request, 'successful.html', {'book': book, 'action': 'is visible'}))
    else:
        return HttpResponse(render(request, "You haven't a permission show this book"))


@login_required
def show_all_books(request, pk):
    books = Book.objects.filter(user=pk)
    if request.user == books.first().user:
        for book in books:
            book.is_visible = True
            book.save()
        return HttpResponse(render(request, 'successful.html', {'book': book, 'action': 'is visible'}))
    else:
        return HttpResponse(render(request, "You haven't a permission show this book"))


@login_required
def add_to_wish_list(request, pk):
    book = Book.objects.get(id=pk)
    user = User.objects.get(username=request.user)
    wishlist = WishList(user_id=user.id, book_id=book.id)
    wishlist.save()
    return HttpResponse(render(request, 'successful.html', {'book': book, 'action': 'was added into wish list'}))


@login_required
def show_wish_list(request):
    user = User.objects.get(username=request.user)
    wishlist = WishList.objects.filter(user=user.id).filter(book__is_visible=True)
    return HttpResponse(render(request, 'wishlist.html', {'object_list': wishlist}))
