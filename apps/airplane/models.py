from django.db import models
from slugify import slugify
from django.contrib.auth import get_user_model


User = get_user_model()


class Producer(models.Model):
    user = models.ForeignKey(
        to=User ,
        on_delete = models.DO_NOTHING,
    )
    title = models.CharField(max_length=50)
    about = models.TextField()
    image = models.ImageField(upload_to='Producer_images')
    slug = models.SlugField(primary_key=True, blank=True, max_length=120)        
    ceo = models.CharField(max_length=101, blank=True)   

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) 
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title 
    
    class Meta:
        verbose_name = 'Producer'
        verbose_name_plural = 'Producers'


class Airplane(models.Model):
    STATUS_CHOICES = (             
        ('archive', 'Archived'),
        ('avail', 'Available')
    )
    user = models.ForeignKey(
        to=User ,
        on_delete = models.DO_NOTHING,
    )
    
    
    title = models.CharField(max_length=70)
    producer = models.ForeignKey(
        to=Producer,
        related_name='Airplane_producers',
        on_delete=models.CASCADE
    )
    desc = models.CharField(max_length=200)
    image = models.ImageField(upload_to='airplane_images')
    year_publ = models.CharField(max_length=4)
    slug = models.SlugField(primary_key=True, blank=True, max_length=80)
    status = models.CharField(choices=STATUS_CHOICES, max_length=9)       
    airplane = models.FileField(upload_to='airplane_files', blank=True)    
    type = models.ManyToManyField(
        to='Type',
        related_name='airplane_type'
    )                   
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)   
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.title}'
    
    class Meta:
        verbose_name = 'Airplane'
        verbose_name_plural = 'Airplanes'


class Type(models.Model):
    user = models.ForeignKey(
        to=User ,
        on_delete = models.DO_NOTHING,
    )
    type = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(primary_key=True, blank=True, max_length=25)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.type)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.type
    
    class Meta:
        verbose_name = "type"
        verbose_name_plural = "types"