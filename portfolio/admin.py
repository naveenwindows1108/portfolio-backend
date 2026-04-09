from django.contrib import admin
from .models import Profile, Skill, Technology, Tag, Project, ProjectImage, Contact


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "title", "email", "location")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    list_filter = ("category",)
    search_fields = ("name",)


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ("name",)


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "is_featured", "is_active", "created_at")
    list_filter = ("status", "is_featured", "is_active", "technologies")
    search_fields = ("title", "description")

    prepopulated_fields = {"slug": ("title",)}

    autocomplete_fields = ["technologies", "tags"]

    inlines = [ProjectImageInline]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("email", "subject", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject")
    readonly_fields = (
        "name",
        "email",
        "subject",
        "message",
        "created_at",
    )
