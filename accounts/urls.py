from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as authViews


app_name= 'accounts'


urlpatterns = [
    path('register/', views.register_1, name= 'register'),
    path('login/', views.login_1, name= 'login'),
    path('logout/', views.logout_1, name= 'logout'),
    path('user/' ,views.userProfile, name="user_profile"),
    path('profile/' ,views.profileinfo, name="profile_info"),
    

    path('reset_password/' ,authViews.PasswordResetView.as_view(template_name= "registration/password_reset.html") , name="reset_password"),
    path('reset_password_sent/' ,authViews.PasswordResetDoneView.as_view(template_name= "registration/password_reset_sent.html") , name="password_reset_done"),
    path('reset/<uidb64>/<token>/' ,authViews.PasswordResetConfirmView.as_view(template_name= "registration/password_reset_form.html") , name="password_reset_confirm"),
    path('reset_password_complete/' ,authViews.PasswordResetCompleteView.as_view(template_name= "registration/password_reset_done.html") , name="password_reset_complete"),

]