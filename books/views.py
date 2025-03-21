from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Author, Book, Member, Borrow
from books.serializers import AuthorSerializer, BookSerializer, MemberSerializer, BorrowSerializer
from django.utils import timezone
from django.shortcuts import get_object_or_404

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class BorrowViewSet(viewsets.ModelViewSet):
    serializer_class = BorrowSerializer
    queryset = Borrow.objects.all()

    def return_book(self, request, pk=None):
        borrow = get_object_or_404(Borrow, pk=pk)
        
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
        borrow.book.availability = True
        borrow.book.save()
        
        return Response({
            "message": "Book returned successfully",
            "fine_amount": float(borrow.fine_amount)
        }, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        book = serializer.validated_data['book']
        book.availability = False
        book.save()
        serializer.save()