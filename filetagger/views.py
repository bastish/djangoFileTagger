# views.py
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, Http404
from .models import AccessibleDirectory, Tag, TagGroup, File
from .forms import DirectoryForm



def directory_list(request):
    if request.method == 'POST':
        form = DirectoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('directory_list')
    else:
        form = DirectoryForm()
    directories = AccessibleDirectory.objects.all()
    return render(request, 'directory_list.html', {'directories': directories, 'form': form})

def directory_detail(request, dir_id):
    directory = get_object_or_404(AccessibleDirectory, id=dir_id)
    # Inside the directory_detail view
    # ...
    if os.path.isdir(directory.path):
        contents = [{'name': item, 'is_dir': os.path.isdir(os.path.join(directory.path, item))}
                    for item in os.listdir(directory.path)]
    else:
        contents = [{'name': 'Invalid directory', 'is_dir': False}]
    return render(request, 'directory_detail.html', {'directory': directory, 'contents': contents})


def gallery_view(request, dir_id, dir_name):
    directory = get_object_or_404(AccessibleDirectory, id=dir_id)
    gallery_path = directory.path
    tags = Tag.objects.all()
    tag_groups = TagGroup.objects.all()

    thumbnails_path = os.path.join(gallery_path, dir_name, 'images/thumbnails')
    photos_path = os.path.join(gallery_path, dir_name, 'images')

    image_data = []

    if os.path.exists(thumbnails_path) and os.path.exists(photos_path):
        thumbnail_files = [name for name in os.listdir(thumbnails_path) if name.endswith('.jpg')]
        photo_files = [name for name in os.listdir(photos_path) if name.endswith('.jpg')]

        for thumbnail, photo in zip(thumbnail_files, photo_files):
            photo_full_path = os.path.join(photos_path, photo)
            file_instance = File.objects.filter(path=photo_full_path).first()
            file_tags = file_instance.tags.all() if file_instance else []

            image_data.append({
                'thumbnail': os.path.join(thumbnails_path, thumbnail),
                'photo': photo_full_path,
                'tags': file_tags
            })
    else:
        image_data = []

    return render(request, 'gallery.html', {
        'gallery_name': gallery_path,
        'images': image_data,
        'tag_groups': tag_groups,
        'tags': tags
    })


def send_image(request, filename):
    image_path = os.path.join('/Volumes/Toshiba 1TB 2022.12.06/flickrBrowser/', filename)
    
    if os.path.exists(image_path) and os.path.isfile(image_path):
        return FileResponse(open(image_path, 'rb'))
    else:
        raise Http404("Image does not exist")

