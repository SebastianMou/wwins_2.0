from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
     path('', views.home, name='home'),
     path('search/<slug:category_slug>/', views.category_list, name='category_list'),
     path('search_p&c/', views.search_pc, name='search_pc'),
     path('complaint/', views.complaint, name='complaint'),
     path('create_category/', views.create_category,    name='create_category'),
     path('home_info/', views.home_info, name='home_info'),
     path('login/', views.login_user, name='login'),
     path('register/', views.register, name='register'),
     path('logout/', views.logout_user, name='logout'),
     path('delete/<int:post_id>/', views.delete, name='delete'),
     path('profile/<username>/', views.profile, name='profile'),
     path('user_profile/<user_id>/', views.user_profile, name='user_profile'),
     path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
     path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
     path('create_post/', views.create_post, name='create_post'),
     path('create_a_goal/', views.create_a_goal, name='create_a_goal'),

     path('all_goals/', views.all_goals, name='all_goals'),
     path('goal_detail/<int:pk>', views.goal_detail, name='goal_detail'),
     path('goal_edit/<int:pk>', views.goal_edit, name='goal_edit'),
     path('goal_delete/<int:goal_id>/', views.goal_delete, name='goal_delete'),
     
     path('post_detail/<int:pk>', views.post_detail, name='post_detail'),
     path('post_edit/<int:pk>', views.post_edit, name='post_edit'),
     path('like_post/<int:pk>/', views.like_post, name='like_post'),
     path('community_guidelines/', views.community_guidelines, name='community_guidelines'),

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
