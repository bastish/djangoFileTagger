# views.py
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, Http404
from .models import AccessibleDirectory, Tag, TagGroup, File
from .forms import DirectoryForm
from django.http import JsonResponse



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
    files_path = os.path.join(gallery_path, dir_name, 'images')

    file_data = []

    if os.path.exists(files_path):
        files = [name for name in os.listdir(files_path) if name.endswith('.jpg')]

        for file in files:
            file_full_path = os.path.join(files_path, file)
            thumbnail_file = file  # assuming thumbnail file has the same name
            thumbnail_path = os.path.join(thumbnails_path, thumbnail_file)

            # Check if the thumbnail exists; if not, use the original file path
            thumbnail_path = thumbnail_path if os.path.exists(thumbnail_path) else file_full_path

            # Check if there's a corresponding File instance in the database
            file_instance = File.objects.filter(path=file_full_path).first()
            file_tags = file_instance.tags.all() if file_instance else []

            file_info = {
                'path': file_full_path,
                'thumbnail': thumbnail_path,
                'tags': file_tags
            }
            file_data.append(file_info)

    return render(request, 'gallery.html', {
        'gallery_name': gallery_path,
        'files': file_data,
        'tag_groups': tag_groups,
        'tags': tags
    })



def send_image(request, filename):
    image_path = os.path.join('/Volumes/Toshiba 1TB 2022.12.06/flickrBrowser/', filename)
    
    if os.path.exists(image_path) and os.path.isfile(image_path):
        return FileResponse(open(image_path, 'rb'))
    else:
        raise Http404("Image does not exist")

