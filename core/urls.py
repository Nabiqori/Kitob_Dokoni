from django.contrib import admin
from django.urls import path

from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.conf.urls.static import static
from django.conf import settings
from rest_framework.generics import UpdateAPIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from main.views import *

schema_view = get_schema_view(
   openapi.Info(
      title="Kitob ddokoni API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('accounts/register/', RegisterAPIView.as_view(), name='register'),
    path('accounts/me/', AccountRetrieveUpdateDestroyAPIView.as_view(), name='update'),
    path('books/', BookListCreateAPIView.as_view(), name='books'),
    path('books/<int:pk>/', BookRetrieveUpdateDestroyAPIView.as_view(), name='book'),
    path('books/mine/', MyBooksList.as_view(), name='mybooks'),
    path('books/<int:pk>/mark-sold/', BookMarkSoldAPIView.as_view(), name='mark-sold'),
    path('accounts/wishlist/', WishlistAPIView.as_view(), name='wishlist'),
    path('accounts/wishlist/<int:pk>/add/', WishlistAddBookAPIView.as_view(), name='wishlist-add'),
    path('accounts/wishlist/<int:pk>/remove/', WishlistRemoveBookAPIView.as_view(), name='wishlist-remove'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)