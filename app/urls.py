from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from app import views



urlpatterns = [
    
    url(r'generate/', views.gen),
    url(r'check/', views.check),
    url(r'assign/', views.assign),
    url(r'unassign/', views.unassign),
    url(r'tokenRefresh/', views.tokenRefresh),
    url(r'delete/', views.deleteToken)
    
]
