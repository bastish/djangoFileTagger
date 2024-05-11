from django.core.management.base import BaseCommand
from filetagger.models import File  # Import your model

class Command(BaseCommand):
    help = 'Updates the file paths in the database'

    def handle(self, *args, **kwargs):
        photos = File.objects.all()
        for photo in photos:
            # Replace the old path with the new path
            photo.path = photo.path.replace('/Volumes/Toshiba 1TB 2022.12.06', '/Volumes/Toshiba1TB20221206')
            photo.save()
            print(f'Updated: {photo.path}')  # Optional: print updated paths

        self.stdout.write(self.style.SUCCESS('Successfully updated all paths.'))
