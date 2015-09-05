from django.contrib import admin

# Register your models here.
from .models import Notes, Category

admin.site.register(Notes)
admin.site.register(Category)
