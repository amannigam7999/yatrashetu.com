from django.conf import settings
from django.conf.urls.static import static

"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.perent,name='perent'),
    # path('ln/',views.login,name='login'),
    path('login/', views.login_view, name='login'),
    path('log/', views.Contact_to_log, name='CTL'),
    path('feed/', views.feed_view, name='feed'),
    path('top/', views.back_to_top, name='top'),
    path('search/', views.search_view, name='search'),
    path('routes/', views.routes, name='routes'),
    path('gride/',views.gallery, name='gride'),
    path('addpost/',views.add_post, name='add_post'),
     path('booking/', views.booking, name='booking'),
    path('book-bus/', views.bus_booking, name='bus_booking'),
    path('feedback/', views.submit_feedback, name='submit_feedback'),
  
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    