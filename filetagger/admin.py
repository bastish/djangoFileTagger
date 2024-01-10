from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import AccessibleDirectory,File, Tag, TagGroup

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'path', 'display_tags')  
    search_fields = ('name', 'path')
    filter_horizontal = ('tags',)

    def display_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')

@admin.register(TagGroup)
class TagGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('tags',)


@admin.register(AccessibleDirectory)
class AccessibleDirectoryAdmin(admin.ModelAdmin):
    list_display = ('path',)