from django.contrib import admin

from .models import Comment, Deceased


@admin.register(Deceased)
class DeceasedAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'short_message',
        'image_tag',
        'approved',
        'archived',
        'date_created',
    )
    list_filter = (
        'approved',
        'archived',
    )
    search_fields = (
        'id',
        'name',
        'country',
        'slug',
    )
    actions = (
        'make_approved',
        'make_unapproved',
    )
    readonly_fields = (
        'comment_url',
    )

    def make_approved(self, request, queryset):
        queryset.update(approved=True)
        self.message_user(request, "Records approved.")
    make_approved.short_description = 'Approve selected'

    def make_unapproved(self, request, queryset):
        queryset.update(approved=False)
        self.message_user(request, "Records unapproved.")
    make_unapproved.short_description = 'Un-approve selected'

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions['delete_selected'][0].short_description = "Delete Selected"
        return actions


@admin.register(Comment)
class CampaignCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'deceased',
        'author',
        'message',
        'date_created',
    )
    search_fields = (
        'deceased__slug',
        'deceased__id',
    )
