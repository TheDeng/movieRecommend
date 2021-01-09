from django.urls import path
from movie import views


urlpatterns = [
    path('list/',views.list_view),
    path('listByTag/',views.listbytag_view),
    path('info/',views.info_view),
    path('update/',views.update_view),
    path('high/',views.hign_view),
    path('recommend/',views.recommend_view),
]