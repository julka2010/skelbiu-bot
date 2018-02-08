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
    actions = ['make_active', 'make_inactive']
    list_display = ('title', 'active')

    def message_success(self, request):
        self.message_user(request, "Success")

    def make_active(self, request, queryset):
        queryset.update(active=True)
        self.message_success(request)
    make_active.short_description = "Mark selected ads for uploading"

    def make_inactive(self, request, queryset):
        queryset.update(active=False)
        self.message_success(request)
    make_inactive.short_description = "Ignore selected ads"


admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(PhoneModel)
