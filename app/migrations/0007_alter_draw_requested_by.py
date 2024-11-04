# Generated by Django 3.2.4 on 2024-11-04 09:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0006_draw_requested_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='draw',
            name='requested_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='draws', to=settings.AUTH_USER_MODEL),
        ),
    ]
