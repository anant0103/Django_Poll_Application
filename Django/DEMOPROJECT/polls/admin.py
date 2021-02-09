from django.contrib import admin
from .models import Question,Choice
#Register your models here.

class Choiceinline(admin.TabularInline):
    model = Choice

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'],'classes':['collapse']}),
    ]
    inlines = [Choiceinline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']

admin.site.register(Question,QuestionAdmin)