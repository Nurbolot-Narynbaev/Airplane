from django.contrib import admin

from .models import (
    Producer, # """author"""
    Airplane, #"""book"""
    Type #"""genre"""
)

admin.site.register(Producer)
admin.site.register(Airplane)
admin.site.register(Type)