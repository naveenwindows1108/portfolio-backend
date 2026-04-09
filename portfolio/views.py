from rest_framework import viewsets, mixins
from .models import Profile, Skill, Project, Contact
from .serializers import (
    ProfileSerializer,
    SkillSerializer,
    ProjectSerializer,
    ContactSerializer,
)


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class SkillViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.active_objects.prefetch_related(
        "images", "technologies", "tags"
    ).all()
    serializer_class = ProjectSerializer
    lookup_field = "slug"  # Changes the URL from /projects/1/ to /projects/my-slug/


class ContactViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
