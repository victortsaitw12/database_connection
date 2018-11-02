from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('render', views.render, name='render'),
    path('query', views.query),
    path('search', views.search)
]
