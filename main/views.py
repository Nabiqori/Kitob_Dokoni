from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS, AllowAny
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from rest_framework.pagination import PageNumberPagination

class MyPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100
class RegisterAPIView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def perform_create(self, serializer):
        serializer.save()
        Wishlist.objects.create(account=serializer.instance)

class AccountRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountSerializer
    def get_object(self):
        return self.request.user

class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['cover', 'account', 'sold']
    search_fields = ['title']
    ordering_fields = ['title', 'price', 'created_at']
    pagination_class = MyPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='sold',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
                description='Filter by sold books'
            ),
            openapi.Parameter(
                name='account',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='Filter by account'
            ),
            openapi.Parameter(
                name='cover',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Filter by cover'
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return BookSerializer
        else:
            return BookPostSerializer
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated()]
    def perform_create(self, serializer):
        serializer.save(account=self.request.user)

class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return BookSerializer
        else:
            return BookPostSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated()]
    def perform_update(self, serializer):
        book = serializer.instance
        if book.account != self.request.user:
            raise PermissionDenied(detail='You do not have permission to perform this action.')
        serializer.save()
    def peform_destroy(self, instance,):
        if instance.account != self.request.user:
            raise PermissionDenied(detail='You do not have permission to perform this action.')
        instance.delete()
class MyBooksList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['cover', 'sold']
    search_fields = ['title']
    ordering_fields = ['title', 'price', 'created_at']
    pagination_class = MyPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='sold',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
                description='Filter by sold books'
            ),
            openapi.Parameter(
                name='cover',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Filter by cover'
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    def get_queryset(self):
        return Book.objects.filter(account=self.request.user)

class BookMarkSoldAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        serializer = BookMarkSoldSerializer(book, data=request.data, account=request.user)
        if serializer.is_valid():
            serializer.save(sold=True)
            responce = {'succes': True, 'message': 'Book marked as sold.', "data": BookSerializer(book).data}
            return Response(responce, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WishlistAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookSerializer
    pagination_class = MyPagination

    def get_queryset(self):
        wishlist = Wishlist.objects.get(account=self.request.user)
        return wishlist.books.order_by('title')

class WishlistAddBookAPIView(APIView):
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        wishlist = Wishlist.objects.get(account=self.request.user)
        wishlist.books.add(book)
        wishlist.save()
        return Response({'succes': True, 'message': 'Book added to wishlist.'}, status=status.HTTP_201_CREATED)

class WishlistRemoveBookAPIView(APIView):
    def delete(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        wishlist = Wishlist.objects.get(account=self.request.user)
        wishlist.books.remove(book)
        wishlist.save()
        return Response({'succes': True, 'message': 'Book removed from wishlist.'}, status=status.HTTP_204_NO_CONTENT)

