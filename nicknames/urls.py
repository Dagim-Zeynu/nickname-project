from django.urls import path
from . import views

app_name = 'nicknames'

urlpatterns = [
    path('', views.home, name='home'),
    path('departments/', views.department_list, name='department_list'),
    path('department/<int:department_id>/', views.student_list, name='student_list'),
    path('student/<int:student_id>/nickname/', views.give_nickname, name='give_nickname'),
    path('student/<int:student_id>/', views.student_detail, name='student_detail'),
    path('nickname/<int:nickname_id>/react/<str:reaction_type>/', views.add_reaction, name='add_reaction'),
    path('student/<int:student_id>/rate/', views.add_rating, name='add_rating'),
    path('terms/', views.terms, name='terms'),
    path('nickname/<int:nickname_id>/report/', views.report_nickname, name='report_nickname'),
] 