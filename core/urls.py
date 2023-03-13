
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [

    re_path(r'^static/(?P<path>.*)$', serve,
        {'document_root': settings.STATIC_ROOT}),

    path('admin/', admin.site.urls),
    path('', include('mysite.urls' , namespace='mysite')),
    path('account/', include('account.urls', namespace='account')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
