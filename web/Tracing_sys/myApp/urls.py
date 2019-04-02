from django.urls import path,re_path
from . import views
urlpatterns = [
    path('',views.index),
    re_path('(\d+)/(\d+)/',views.detail),

    path('poems',views.tracing_poems),
]