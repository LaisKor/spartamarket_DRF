import os
from django.db import models
from django.conf import settings

class Product(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='products/MEDIA')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='products', on_delete=models.CASCADE)

    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs) 

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_file = Product.objects.get(pk=self.pk).image
                if old_file and old_file != self.image:
                    if os.path.isfile(old_file.path):
                        os.remove(old_file.path)
            except Product.DoesNotExist:
                pass 
        super().save(*args, **kwargs) 


