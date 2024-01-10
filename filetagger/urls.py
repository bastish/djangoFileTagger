from django.urls import path
from .views import directory_list, directory_detail, gallery_view, send_image
from .views_api import search_by_tags_html, update_file_tags, create_tags, get_photo_tags, search_by_tags

urlpatterns = [
    path('directories/', directory_list, name='directory_list'),
    path('directories/<int:dir_id>/', directory_detail, name='directory_detail'),       
    path('gallery/<int:dir_id>/<str:dir_name>/', gallery_view, name='gallery_view'),    
    path('image/<path:filename>/', send_image, name='send_image'),
    path('api/update-file-tags/', update_file_tags, name='update_file_tags'),
    path('api/create-tags/', create_tags, name='create_tags'),
    path('api/get-photo-tags/', get_photo_tags, name='get_photo_tags'),
    path('api/search-by-tags/', search_by_tags, name='search_by_tags'),
    path('api/search-by-tags-html/', search_by_tags_html, name='search_by_tags_html'),

]
