from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import File, Tag
import json
import os
from django.shortcuts import render

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

        # If the File is newly created, set its name
        if created:
            file.name = os.path.basename(photo_path)
            file.save()

        tags = Tag.objects.filter(id__in=tag_ids)

        
        if action == 'add':
            file.tags.add(*tags)
        elif action == 'remove':
            file.tags.remove(*tags)

        updated_tags = list(file.tags.values('id', 'name'))

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
    

def search_by_tags(request):
    tag_ids = request.GET.get('tag_ids', '').split(',')
    files = File.objects.filter(tags__id__in=tag_ids).distinct() if tag_ids else File.objects.none()
    
    image_data = [{'thumbnail': file.path, 'photo': file.path, 'id': file.id} for file in files]
    return JsonResponse({'images': image_data})


def gallery_item_html(request, file_id):
    file_instance = File.objects.get(id=file_id)
    return render(request, 'gallery_item.html', {'file': file_instance})

def search_by_tags_html(request):
    tag_ids = request.GET.get('tag_ids', '').split(',')
    files = File.objects.filter(tags__id__in=tag_ids).distinct() if tag_ids else File.objects.none()

    return render(request, 'gallery_items.html', {'files': files})

