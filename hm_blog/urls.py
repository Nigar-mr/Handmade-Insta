from django.conf.urls import url
from django.urls import path, include
from .views import home, register, verify_view, profile, logout_page, \
    add_shot, profile_settings, social_settings, explore, picture_add, \
    picture_delete, about, into_shot, FollowView, FollowingView, \
    FollowersView, ContactView
from django.views.generic import TemplateView

urlpatterns = [
    path('', home, name='home'),
    path('explore/', explore, name='explore'),
    path('register/', register, name='register'),
    path('verify/<str:token>/<int:user_id>/', verify_view, name='verify_view'),
    path('profile/<int:id>/', profile, name='profile'),
    path('upload/image', picture_add, name='picture-add'),
    path('delete/image', picture_delete, name="picture-delete"),
    path('logout/', logout_page, name="logout"),
    path('add/', add_shot, name='add'),
    path('profile-settings/', profile_settings, name='profile-settings'),
    path('social-settings/', social_settings, name='social-settings'),
    path('about/', about, name='about'),
    path('into_shot/<int:id>', into_shot, name='into-shot'),
    path('follow/', FollowView.as_view(), name='follow'),
    path('<int:id>/following/', FollowingView, name='following'),
    path('<int:id>/followers/', FollowersView, name='followers'),
    path('comment/', into_shot, name='comment'),
    path('contact/', ContactView, name='contact')

]
