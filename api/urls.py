from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from books.views import BookViewSet, AuthorViewSet, MemberViewSet, BorrowViewSet

router = DefaultRouter()
router.register('books', BookViewSet, basename='books')
router.register('authors', AuthorViewSet, basename='authors')
router.register('members', MemberViewSet, basename='members')
router.register('borrows', BorrowViewSet, basename='borrows')  

borrows_router = routers.NestedSimpleRouter(
    router, 
    'borrows', 
    lookup='borrow'
)
borrows_router.register('return', BorrowViewSet, basename='borrow-return')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(borrows_router.urls)),
]