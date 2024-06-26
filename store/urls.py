from django.urls import path
from . import views

app_name = "store"
urlpatterns = [
    path(
        '',
        views.StoreCreateView.as_view(),
        name='list'),
    path(
        'create/',
        views.StoreCreateView.as_view(),
        name='create'),
    path(
        '<pk>/update',
        views.StoreUpdateView.as_view(),
        name='update'),
    path(
        '<pk>/details/',
        views.StoreDetailView.as_view(),
        name='details'),
    path(
        '<pk>/delete/',
        views.StoreDeleteView.as_view(),
        name='delete'),
    path(
        '<pk>/piechart/',
        views.StoreListView.demo_piechart,
        name='chart'),
]
