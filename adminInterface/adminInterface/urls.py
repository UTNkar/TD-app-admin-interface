"""adminInterface URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.singIn),
    path(
        'ticket-system/delete-event/<id>',
        views.delete_event,
        name='delete_event'
    ),
    path('ticket-system/new-event/', views.create_event, name='create_event'),
    path(
        'ticket-system/edit-event/<id>',
        views.edit_event,
        name="edit_event"
    ),
    path('ticket-system/', views.ticket_system),
    path('start/', views.start),
    path('login/', views.login_user),
]
