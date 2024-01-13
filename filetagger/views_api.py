from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import File, Tag
import json
import os
from django.shortcuts import render
from .utils import create_or_update_json_for_file


@csrf_exempt
@require_http_methods(["POST"])
def update_file_tags(request):
    try:
        data = json.loads(request.body)
        photo_path = data.get('photo')
        tag_ids = data.get('tags', [])
        action = data.get('action', 'add')

        # Check if the File exists based on the path
        file, created = File.objects.get_or_create(path=photo_path)

        if created:
            file.name = os.path.basename(photo_path)
            file.save()

        tags = Tag.objects.filter(id__in=tag_ids)

        if action == 'add':
            file.tags.add(*tags)
        elif action == 'remove':
            file.tags.remove(*tags)

        updated_tags = list(file.tags.values('id', 'name'))

        if file:
            create_or_update_json_for_file(file)

        return JsonResponse({
            "status": "success", 
            "message": f"Tags {action}ed successfully",
            "updatedTags": updated_tags
        })
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)



@csrf_exempt
@require_http_methods(["POST"])
def create_tags(request):
    try:
        data = json.loads(request.body)
        tag_names = data.get('tags', [])

        new_tags = []
        for name in tag_names:
            tag, created = Tag.objects.get_or_create(name=name)
            if created:
                new_tags.append({'id': tag.id, 'name': tag.name, 'slug': tag.slug})

        return JsonResponse({'new_tags': new_tags})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)



@require_http_methods(["GET"])
def get_photo_tags(request):
    photo_path = request.GET.get('photo')
    try:
        file = File.objects.get(path=photo_path)
        tags = list(file.tags.values('id', 'name'))
        return JsonResponse({'tags': tags})
    except File.DoesNotExist:
        return JsonResponse({'tags': []})
    


def search_by_tags_html(request):
    tag_ids = request.GET.get('tag_ids', '').split(',')
    files = File.objects.filter(tags__id__in=tag_ids).distinct() if tag_ids else File.objects.none()

    file_data = []
    for file_instance in files:
        # thumbnail path needs to mirror the photo path with an added 'thumbnails' directory
        thumbnail_path = file_instance.path.replace('/images/', '/images/thumbnails/')
        file_instance.thumbnail = thumbnail_path if os.path.exists(thumbnail_path) else file_instance.path

        file_data.append(file_instance)

    return render(request, 'gallery_items.html', {'files': file_data})


@csrf_exempt
@require_http_methods(["POST"])
def publish_file(request):
    try:
        data = json.loads(request.body)
        file_path = data.get('path')
        print("File path received:", file_path)  # Debugging statement

        try:
            file, created = File.objects.get_or_create(path=file_path)

            #file = File.objects.get(path=file_path)
        except File.DoesNotExist:
            raise ValueError(f"No file found with path: {file_path}")

        file.published = True
        file.save()

        update_published_status(file_path, True)
        add_to_published_list(file_path)

        return JsonResponse({"status": "success", "message": "File published successfully"})
    except Exception as e:
        print("Error:", str(e))  # Print the error for debugging
        return JsonResponse({"status": "error", "message": str(e)}, status=400)



def update_published_status(file_path, status):
    json_file_path = f'{file_path}.json'
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r+') as file:
            data = json.load(file)
            data['published'] = status
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

def add_to_published_list(file_path):
    # Remove the .jpg extension and append .json
    json_file_path = f'{file_path.rsplit(".", 1)[0]}.json'
    published_list_path = os.path.join(os.path.dirname(file_path), 'published.json')

    # Check if the file is already in the list
    if not is_path_in_published_list(json_file_path, published_list_path):
        with open(published_list_path, 'a') as file:
            file.write(f'{json_file_path}\n')

def is_path_in_published_list(json_file_path, published_list_path):
    if os.path.exists(published_list_path):
        with open(published_list_path, 'r') as file:
            if json_file_path in file.read():
                return True
    return False

