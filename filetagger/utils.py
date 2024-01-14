import os
import json

def create_or_update_json_for_file(file_instance):
    if not file_instance:
        return

    file_tags = file_instance.tags.all()

    # Create JSON data for the file
    json_data = {
        "id": file_instance.id,
        "name": os.path.basename(file_instance.path),
        "path": file_instance.path,
        "tags": [{"id": tag.id, "name": tag.name} for tag in file_tags]
    }

    file_path = f'{file_instance.path}'
    json_filename = f'{file_path.rsplit(".", 1)[0]}.json'

    with open(json_filename, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)
