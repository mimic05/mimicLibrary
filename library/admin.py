from django.contrib import admin
from .models import Book, Transaction  # Import your models
from .models import Book, Transaction

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'unique_code', 'is_available')  # Customize the columns in the list view
    fields = ('title', 'author', 'unique_code', 'description', 'is_available')  # Specify fields to display in the admin form

admin.site.register(Book, BookAdmin)
admin.site.register(Transaction)
