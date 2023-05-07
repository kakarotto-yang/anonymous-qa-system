from django.urls import path,include
import board.views

urlpatterns =[
    path('ask/', board.views.ask_question),
    path('host/answer/', board.views.host_answer),
    path('answer/', board.views.answer),
    path('list/', board.views.show_mes),
    path('changeBoardIfo/', board.views.changeBoardIfo),
    path('success/', board.views.success),
    path('error/', board.views.error),
    path('login/', board.views.login_view),
]