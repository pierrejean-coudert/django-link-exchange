from django.db import models
from django.contrib import admin

from link_exchange.models import Campaign, Link


def check_backlinks(modeladmin, request, queryset):
    """
    Admin action : check if selected backlinks are active
    """
    for l in queryset:
        l.check_backlink()
check_backlinks.short_description = "Check selected back links"

def make_active(modeladmin, request, queryset):
    """
    Admin action : activate selected links
    """
    queryset.update(active=True)
make_active.short_description = "Mark selected links as active"

def make_inactive(modeladmin, request, queryset):
    """
    Admin action : deactivate selected links
    """
    queryset.update(active=False)
make_inactive.short_description = "Mark selected links as inactive"
        
class LinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'campaign', 'anchor', 'external_url', 'active', 'checked_ok', 
                    'last_checked', 'checked_message')
    search_fields = ['name', 'anchor',]
    list_filter = ['campaign', 'active', 'checked_ok']
    actions = [make_active, make_inactive, check_backlinks] 
    fieldsets = (
        (None, {
            'fields': ('name', 'campaign')
        }),
        ('Link configuration', {
            'fields': ('anchor', 'external_url', 'text', 'active')
        }),
        ('BackLink configuration', {
            'fields': ('reverse_url','reverse_anchor','reverse_dest_url')
        }),
        ('BackLink verification', {
            'fields': ('checked_ok','checked_message')
        }),
    )

        
class LinkInline(admin.TabularInline):
    model = Link
    exclude = ['checked_ok', 'last_checked',]

class CampaignAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('title', 'main_url', 'contact_name', 'update_date')
    search_fields = ['title', 'main_url',]
    fieldsets = (
        (None, {
            'fields': ('title', 'main_url')
        }),
        ('Contact', {
            'fields': ('contact_name', 'contact_email')
        }),
        ('Advanced options', {
            'fields': ('css_class', 'more_attribute', 'target')
        }),
    )
    inlines = [
        LinkInline,
    ]   

admin.site.register(Campaign, CampaignAdmin)    
admin.site.register(Link, LinkAdmin)    