from django.urls import path
from muser import views

urlpatterns = [
    path('login/',views.login_view),
    path('logout/',views.login_out_view),
    path('register/',views.register_view),
]