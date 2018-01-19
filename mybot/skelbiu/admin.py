from django.contrib import admin

from .models import (
    Advertisement,
    AdvertisementImage,
    PhoneModel,
)

class AdvertisementImageInline(admin.TabularInline):
    model = AdvertisementImage
    extra = 3


class AdvertisementAdmin(admin.ModelAdmin):
    inlines = [AdvertisementImageInline]


admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(PhoneModel)
