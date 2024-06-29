from rest_framework.routers import DefaultRouter
from django.urls import include, path

from authentication.views import UserViewSet
from story.views import StoryApi
from personalize.views import PersonalizeApi

router = DefaultRouter()

router.register("auth", UserViewSet, basename="auth")
router.register("story", StoryApi, basename="story")
router.register("personalize", PersonalizeApi, basename="personalize")

urlpatterns = [
    path("", include(router.urls)),
]