"""csvt01 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/$', 'blog.views.index'),
    url(r'^newGame/$', 'blog.views.newGame'),
    url(r'^newGame/input/$', 'blog.views.newGame_input'),
    url(r'^newGame/inputData/$', 'blog.views.newGame_inputData'),
    url(r'^newGame/over/$', 'blog.views.newGame_over'),
    url(r'^newGame/view/$', 'blog.views.newGame_view'),
    url(r'^oldGame/$', 'blog.views.oldGame'),
    url(r'^oldGame/viewHistoryData/$', 'blog.views.viewHistoryData'),
    url(r'^playerData/$', 'blog.views.playerData'),
    url(r'^playerRanking/$', 'blog.views.playerRanking'),
]
