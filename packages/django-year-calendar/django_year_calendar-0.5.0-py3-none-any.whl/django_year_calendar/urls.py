from django.urls import path

from .views import CalendarView, SelectionView

urlpatterns = [
    path('', CalendarView.as_view()),
    path('select/<int:start>/<int:end>',       SelectionView.as_view(template_name='django_year_calendar/select_add.html')),
    path('select/<req>/<int:start>/<int:end>', SelectionView.as_view()),
]