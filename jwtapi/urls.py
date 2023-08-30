from django.urls import path
from jwtapi import views
urlpatterns = [
    path('registeration/', views.UserRegisteration.as_view()),
    path('login/', views.UserLoginView.as_view()),
    path('profile/', views.UserProfileView.as_view()),
    path('changePassword/', views.UserChangePasswordView.as_view())
]
