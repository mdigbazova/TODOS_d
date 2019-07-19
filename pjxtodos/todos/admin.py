from django.contrib import admin

from . models import Todo, Profile

# Register your models here.


class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date',)


admin.site.register(Todo)
admin.site.register(Profile)
