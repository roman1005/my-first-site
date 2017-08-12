from django.contrib import admin
from .models import News, Comment, Paragraph, Tag


class ParagraphInline(admin.StackedInline):
    model = Paragraph
    extra = 1

class TagInline(admin.StackedInline):
    model = Tag
    extra = 1


class CommentsInLine(admin.StackedInline):
    model = Comment
    extra = 0


class NewsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('heading',)}
    inlines = [ParagraphInline,TagInline,CommentsInLine]
# Register your models here.
admin.site.register(News, NewsAdmin)

# Register your models here.
