# Django
from django.urls import include, path
# Project
from . import views

app_name="accounts"
urlpatterns = [
    path('signup/', views.UserCreateView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('password_reset/', views.UserResetPasswordView.as_view(), name="password_reset"),
    path('password_reset/done/', views.UserResetPasswordDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.UserResetPasswordConfirmView.as_view(),name='password_reset_confirm'),
    path('password_reset_complete/', views.UserResetPasswordCompleteView.as_view(),name='password_reset_complete'),
    path('profile/<pk>', views.UserDetailView.as_view(), name='profile'),
]
