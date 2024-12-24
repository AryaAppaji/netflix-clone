# Generated by Django 5.1.4 on 2024-12-24 11:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('finance', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_mode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_mode', to='finance.paymentmode'),
        ),
        migrations.AddField(
            model_name='payment',
            name='subscription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscription', to='finance.subscription'),
        ),
        migrations.AddField(
            model_name='usersubscription',
            name='subscription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscription_details', to='finance.subscription'),
        ),
        migrations.AddField(
            model_name='usersubscription',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_subscription', to=settings.AUTH_USER_MODEL),
        ),
    ]