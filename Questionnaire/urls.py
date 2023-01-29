from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

from user import views
from django.views.static import serve 

urlpatterns = [
     path('admin/', admin.site.urls),
     path('api/user/', include('user.api.urls')),
     path('api/', include('post.api.urls')),
     path('', include('post.urls')),


     path('login/', views.userlogin, name='login'),
     path('logout/', views.userlogout, name='logout'),
     path('signup/', views.registrer, name='signup'),
     path('profile/', views.userprofile, name='profile'),
     path('profile/update/', views.userupdateprofile, name='profileupdate'),

     # password reset
     path('reset_password/',
          auth_views.PasswordResetView.as_view(),         name='reset_password'),
     path('reset_password_sent/',
          auth_views.PasswordResetDoneView.as_view(),     name='password_reset_done'),
     path('reset/<uidb64>/<token>/',
          auth_views.PasswordResetConfirmView.as_view(),  name='password_reset_confirm'),
     path('reset_password_complete/',
          auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]

urlpatterns += re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
