from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import File, Tag
import json
import os

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
            message = "Tags added successfully"
        elif action == 'remove':
            file.tags.remove(*tags)
            message = "Tags removed successfully"

        return JsonResponse({"status": "success", "message": message})
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


