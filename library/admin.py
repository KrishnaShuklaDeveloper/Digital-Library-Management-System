from django.contrib import admin
from .models import Member, Book, Transaction, Fine  # Ensure UserProfile is listed here

admin.site.register(Member)
admin.site.register(Book)
admin.site.register(Transaction)
admin.site.register(Fine)