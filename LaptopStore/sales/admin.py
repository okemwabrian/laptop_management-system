from django.contrib import admin
from .models import Laptop, Sale, ContactMessage

class LaptopAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'price', 'stock', 'image')  
    search_fields = ('brand', 'model')  
    list_filter = ('brand',)  
    ordering = ('brand',)  
    list_per_page = 20  

admin.site.register(Laptop, LaptopAdmin)

class SaleAdmin(admin.ModelAdmin):
    list_display = ('laptop', 'quantity', 'date')  
    search_fields = ('laptop__model',)  
    list_filter = ('date',)  
    ordering = ('-date',)  
    date_hierarchy = 'date'  

admin.site.register(Sale, SaleAdmin)

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'created_at')  
    search_fields = ('name', 'email')  
    list_filter = ('created_at',)  
    ordering = ('-created_at',)  
admin.site.register(ContactMessage, ContactMessageAdmin)
