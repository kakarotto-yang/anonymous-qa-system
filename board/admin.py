from django.contrib import admin

# Register your models here.
from board.models import Question, BoardIfo

admin.site.register(Question)

admin.site.register(BoardIfo)