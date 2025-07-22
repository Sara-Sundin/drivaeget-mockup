from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # 👈 bloggen visas direkt på /
    path('summernote/', include('django_summernote.urls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

