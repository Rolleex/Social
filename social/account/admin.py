from django.contrib import admin
from .models import Profile, Follow


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'profile_pic', 'slug']
    prepopulated_fields = {'slug': ('user',)}


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Follow)