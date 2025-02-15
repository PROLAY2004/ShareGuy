"""
URL configuration for ShareGuy_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from Main_app import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="Index"),
    path('Home', views.home, name="Home"),
    path('About', views.about, name="About"),
    path('Contact', views.contact, name="Contact"),
    path('Download/<str:code>', views.qr_download, name="Download_by_Qr"),
    # path('Send', views.send, name="Send"),
    # path('Recive', views.recive, name="Recive"),
]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
