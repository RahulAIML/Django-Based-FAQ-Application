from django.contrib import admin

# Register your models here.
# faq/admin.py
from .models import FAQ

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'question_hi', 'question_bn']
