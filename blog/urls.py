from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
     path('', views.home, name='home'),
     path('search/<slug:category_slug>/', views.category_list,    name='category_list'),
     path('create_category/', views.create_category,    name='create_category'),
     path('home_info/', views.home_info, name='home_info'),
     path('login/', views.login_user, name='login'),
     path('register/', views.register, name='register'),
     path('logout/', views.logout_user, name='logout'),
     path('delete/<int:post_id>/', views.delete, name='delete'),
     path('profile/<username>/', views.profile, name='profile'),
     path('user_profile/<user_id>/', views.user_profile, name='user_profile'),
     path('create_post/', views.create_post, name='create_post'),
     path('post_detail/<int:pk>', views.post_detail, name='post_detail'),
     path('post_edit/<int:pk>', views.post_edit, name='post_edit'),
     path('like_post/<int:pk>/', views.like_post, name='like_post'),

     path('activate/<uidb64>/<token>', views.activate, name='activate'),

     path('password_reset/', auth_view.PasswordResetView.as_view(template_name='blog/users/password_reset.html'),
          name='password_reset'),
     path('password_reset_done/', auth_view.PasswordResetDoneView.as_view(template_name='blog/users/password_reset_done.html'),
          name='password_reset_done'),
     path('password_reset_confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='blog/users/password_reset_confirm.html'),
          name='password_reset_confirm'),
     path('password_reset_complete/', auth_view.PasswordResetCompleteView.as_view(template_name='blog/users/password_reset_complete.html'),
          name='password_reset_complete'),
]
