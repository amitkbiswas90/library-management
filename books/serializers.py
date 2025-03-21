from rest_framework import serializers
from books.models import Author, Book, Member, Borrow
from user.models import User

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'biography', 'birth_date']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'category', 'availability']


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class MemberSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()
    current_books = serializers.PrimaryKeyRelatedField(
        many=True, 
        read_only=True
    )

    class Meta:
        model = Member
        fields = [
            'id', 
            'user',
            'membership_date',
            'current_books'
        ]
        read_only_fields = ['membership_date']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        
        user = User.objects.create_user(
            email=user_data['email'],
            password=user_data['password'],
            first_name=user_data.get('first_name', ''),
            last_name=user_data.get('last_name', '')
        )
        
        member = Member.objects.create(
            user=user,
            email=user.email,
            **validated_data
        )
        return member

class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = [
            'id', 
            'book', 
            'member', 
            'borrow_date', 
            'due_date', 
            'return_date', 
            'fine_amount'
        ]
        read_only_fields = ['borrow_date', 'fine_amount']