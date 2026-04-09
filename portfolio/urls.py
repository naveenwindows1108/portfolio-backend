from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"profile", views.ProfileViewSet, basename="profile")
router.register(r"skills", views.SkillViewSet, basename="skills")
router.register(r"projects", views.ProjectViewSet, basename="project")
router.register(r"contact", views.ContactViewSet, basename="contact")

urlpatterns = [
    path("api/", include(router.urls)),
]
