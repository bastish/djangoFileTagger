from django.db import models
from django.utils.text import slugify


from django.db import models

class File(models.Model):
    name = models.CharField(max_length=255)
    path = models.TextField()
    tags = models.ManyToManyField('Tag', related_name='files')
    published = models.BooleanField(default=False)


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)


class TagGroup(models.Model):
    name = models.CharField(max_length=100)
    tags = models.ManyToManyField('Tag', related_name='tag_groups')
    

class AccessibleDirectory(models.Model):
    path = models.CharField(max_length=1024)

    def __str__(self):
        return self.path
