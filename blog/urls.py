from django.conf import settings
from django.urls import path
from django.views.generic import TemplateView
from blog.views import ProfileView, AddView, Update, DeletePhoto
from django.conf.urls.static import static

urlpatterns = [
    path('<str:username>/', ProfileView.as_view(template_name='profile.html'), name='profile'),
    path('buscar', TemplateView.as_view(template_name='index.html'),name='buscar'),
    path('<str:username>/add/', AddView.as_view(template_name='crud/add.html'), name='add'),
    path('<str:username>/<pk>/update', Update.as_view(template_name="crud/edit.html"), name="update"), 
    path('<str:username>/<pk>/delete', DeletePhoto.as_view(template_name="crud/delete.html"), name="delete"), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)