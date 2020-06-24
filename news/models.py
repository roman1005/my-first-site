from django.db import models
from django.contrib.auth.models import User


class News(models.Model):
    author = models.ForeignKey(User, models.deletion.CASCADE)
    heading = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    STATUS_CHOICES = (
    ('Art', 'Art'), ('Sport', 'Sport'), ('Science', 'Science'), ('Politics', 'Politics'), ('Trips', 'Trips'))
    departments = ["Art", "Politics", "Sport", "Science","Trips"]
    department = models.CharField(max_length=15, choices=STATUS_CHOICES, default=STATUS_CHOICES[0])
    published_time = models.DateTimeField()

    class Meta():
        get_latest_by = 'published_time'
        ordering=('-published_time',)


class Paragraph(models.Model):
            class Meta():
                db_table = 'paragraphs'

            paragraph = models.TextField(max_length=20000, null=True, blank=True)
            image = models.ImageField(upload_to='images/', null=True, blank=True)
            image_description = models.CharField(max_length=200, null=True, blank=True)
            news_paragraph = models.ForeignKey("News", models.deletion.CASCADE)


class Tag(models.Model):
        class Meta():
            db_table = 'tags'

        tag = models.CharField(max_length=120, default='')
        news_tag = models.ForeignKey("News", models.deletion.CASCADE)


class Comment(models.Model):
    comments_news=models.ForeignKey(News, models.deletion.CASCADE)
    published_time = models.DateTimeField()
    body=models.TextField()
    comments_user=models.ForeignKey(User, models.deletion.CASCADE)

    class Meta():
        ordering=('-published_time',)





# Create your models here.
