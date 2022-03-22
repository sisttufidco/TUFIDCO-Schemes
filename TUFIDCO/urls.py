"""TUFIDCO URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.views.static import serve as mediaserve
from TUFIDCOapp.forms import PlaceholderAuthForm
admin.autodiscover()

urlpatterns = [
    path('', include('TUFIDCOapp.urls')),
    path('ULBFOrms', include('ULBForms.urls')),
    path('admin/reports', include('reports.urls')),
    path('Dashboard/', include("Dashboard.urls")),
    path('admin/login/', auth_views.LoginView.as_view(template_name='pages/admin_login.html',
                                                      authentication_form=PlaceholderAuthForm,
                                                      redirect_authenticated_user=True), name='login'
         ),
    path('admin/', include('smart_selects.urls')),
    path('admin/', admin.site.urls),
    re_path(f'^{settings.MEDIA_URL.lstrip("/")}(?P<path>.*)$', mediaserve,
            {'document_root': settings.MEDIA_ROOT})
]
