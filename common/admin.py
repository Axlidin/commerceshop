from django.contrib import admin
from common.models import *
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']

class RegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']

class MediaAdmin(admin.ModelAdmin):
    list_display = ['file', 'type']

class SettingAdmin(admin.ModelAdmin):
    list_display = ['home_image', 'home_title', 'home_subtitle']

class OurInstagramStoryAdmin(admin.ModelAdmin):
    list_display = ['image', 'link']

class CustomerFeedbackAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'customer_position', 'rank', 'image']
    search_fields = ['customer_name', 'customer_position', 'rank']
    list_filter = ['rank']

    def has_add_permission(self, request):
        return False

admin.site.register(Country, CountryAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Settings, SettingAdmin)
admin.site.register(OurInstagramStory, OurInstagramStoryAdmin)
admin.site.register(CustomerFeedback, CustomerFeedbackAdmin)