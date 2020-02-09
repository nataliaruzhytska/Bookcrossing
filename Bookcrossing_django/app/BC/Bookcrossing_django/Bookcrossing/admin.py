from django.contrib import admin
from .models import User, Book, Library


# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('first_name', 'last_name', 'email')
#     search_fields = ('first_name', 'last_name', 'email')
#     list_filter = ('last_name', 'email')


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_id')
    search_fields = ('name', 'user_id')
    list_filter = ('name', 'user_id')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'edition', 'year_ed', 'translator', 'lib_id',
                    'user_id', 'is_visible')
    search_fields = ('name', 'author')
    list_filter = ('name', 'author', 'is_visible')
