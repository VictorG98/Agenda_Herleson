from django.conf import settings # novo
from django.conf.urls.static import static # novo
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('contatos.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # novo
