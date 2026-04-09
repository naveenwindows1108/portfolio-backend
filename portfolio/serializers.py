from rest_framework import serializers
from .models import Profile, Skill, Technology, Tag, Project, ProjectImage, Contact


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name", "category"]


class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ["image", "alt_text"]


class ProjectSerializer(serializers.ModelSerializer):

    images = ProjectImageSerializer(many=True, read_only=True)
    technologies = serializers.StringRelatedField(many=True)
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "github_link",
            "live_link",
            "images",
            "technologies",
            "tags",
            "created_at",
        ]


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["name", "email", "subject", "message"]
