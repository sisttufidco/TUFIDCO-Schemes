from django.urls import path
from . import views
from .views import EmailAttachementView, EmailAttachementView2

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('gallery', views.gallery, name='gallery'),
    path('contact', views.contact, name='contact'),
    path('faq', views.FAQ, name='faq'),
    path('schemes/knmt/AtGlance', views.KNMT, name='knmt'),
    path('schemes/knmt/Guidelines', views.KNMT_G, name='knmt_g'),
    path('schemes/Knmt/AdministrativeSanction', views.KNMT_AS, name='knmtAS'),
    path('schemes/singarachennai2.0/AtGlance', views.S_Chennai, name='SChennai2.0'),
    path('schemes/singarachennai2.0/Guidelines', views.S_Chennai_Guidelines, name='SChennaiGuidelines'),
    path('schemes/singarachennai2.0/AdminstrativeSanction', views.S_Chennai_AS, name='SChennaiAS'),
    path('admin/contactDMA', EmailAttachementView.as_view(), name='emailattachment'),
    path('admin/contactCTP', EmailAttachementView2.as_view(), name='emailattachment2'),
]
