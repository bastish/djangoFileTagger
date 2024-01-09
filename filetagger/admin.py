from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import File, Tag, TagGroup

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'path')  
    search_fields = ('name', 'path')
    filter_horizontal = ('tags',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')

@admin.register(TagGroup)
class TagGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('tags',)
