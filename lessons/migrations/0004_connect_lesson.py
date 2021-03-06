# Generated by Django 2.2 on 2020-12-10 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0003_like'),
    ]

    operations = [
        migrations.CreateModel(
            name='Connect_Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=45)),
                ('heading', models.CharField(default='How are these connected?', max_length=45)),
                ('content', models.TextField(default='Share at least one conjecture about how these representations are related.')),
                ('likes_allowed', models.BooleanField(default=False)),
                ('max_likes', models.IntegerField(default=0)),
                ('justification_required', models.BooleanField(default=False)),
                ('justification_text', models.TextField(default='I think this observation is significant because...')),
                ('like_same_day', models.BooleanField(default=False)),
                ('lesson_code', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('lessons', models.ManyToManyField(related_name='connect_lessons', to='lessons.Solo_Lesson')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='connect_lessons', to='lessons.User')),
            ],
        ),
    ]
