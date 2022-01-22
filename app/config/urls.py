from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('daily.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# handler400~500 オーバーライド
# settings.DEBUG = Falseの場合、エラー発生時に下記Viewを優先して使用。
handler404 = 'daily.views.view_error.page_not_found'
handler500 = 'daily.views.view_error.server_error'
