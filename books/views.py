from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import Author, Book, Member, Borrow
from .serializers import AuthorSerializer, BookSerializer, MemberSerializer, BorrowSerializer
from django.utils import timezone
from django.shortcuts import get_object_or_404
from api.permissions import IsLibrarian, IsMember

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated] 
        else:
            permission_classes = [IsLibrarian]  
        return [permission() for permission in permission_classes]

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsLibrarian]  

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = []  
        else:
            permission_classes = [IsLibrarian]  
        return [permission() for permission in permission_classes]

class BorrowViewSet(viewsets.ModelViewSet):
    serializer_class = BorrowSerializer
    queryset = Borrow.objects.all()
    
    def get_permissions(self):
        if self.action in ['create', 'return_book']:
            permission_classes = [IsMember]  
        elif self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]  
        else:
            permission_classes = [IsLibrarian] 
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        borrow = get_object_or_404(Borrow, pk=pk)
        
        if borrow.member.user != request.user and not request.user.is_staff:
            return Response(
                {"error": "You can only return books you borrowed"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if borrow.return_date:
            return Response(
                {"error": "Book already returned"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        borrow.return_date = timezone.now().date()
        
        if borrow.return_date > borrow.due_date:
            days_overdue = (borrow.return_date - borrow.due_date).days
            borrow.fine_amount = days_overdue * 5
        
        borrow.save()
        borrow.member.current_books.remove(borrow.book)
        
        return Response({
            "message": "Book returned successfully",
            "fine_amount": float(borrow.fine_amount)
        }, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        book = serializer.validated_data['book']
        member = self.request.user.member
        
        if not book.availability:
            raise serializers.ValidationError("This book is not available for borrowing")
        
        member.current_books.add(book)
        serializer.save(member=member)