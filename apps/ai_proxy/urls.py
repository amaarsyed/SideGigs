from django.urls import path
from .views import safety_questions, safety_score

urlpatterns = [
    path("safety/questions/", safety_questions),
    path("safety/score/",    safety_score),
]
