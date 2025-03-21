# Generated by Django 5.1.6 on 2025-03-20 23:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrow',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrow_records', to='books.book'),
        ),
        migrations.AlterField(
            model_name='borrow',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrow_history', to='books.member'),
        ),
        migrations.AlterField(
            model_name='member',
            name='current_books',
            field=models.ManyToManyField(blank=True, related_name='current_readers', to='books.book'),
        ),
        migrations.AlterField(
            model_name='member',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='member_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
