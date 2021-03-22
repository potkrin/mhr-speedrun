from django.urls import path
from cms import views


app_name = 'cms'
urlpatterns = [

    # Quests
    path('quest/', views.quest_list, name='quest_list'),    # List
    path('quest/add/', views.quest_edit, name='quest_add'), # add 
    path('quest/mod/<int:quest_id>', views.quest_edit, name='quest_mod'), # modify 
    path('quest/del/<int:quest_id>', views.quest_del, name='quest_del'),  # delete 

    # Records
    # path('record/<int:quest_id>/', views.RecordList.as_view(), name='record_list'),    # List
    path('record/user_submission/', views.usersub_list, name='usersub_list'),    # List
    path('record/<int:quest_id>/<str:party>/<str:weapon>/<str:rule>/<str:platform>/', views.RecordList.as_view(), name='record_list'),    # List
    path('record/<int:quest_id>/<str:party>/<str:rule>/<str:platform>/', views.Summary.as_view(), name='weapon_rank'),    # List
    path('record/add/<int:quest_id>/', views.record_edit, name='record_add'), # add 
    path('record/add/<int:quest_id>/<int:conf>', views.record_edit, name='record_add'), # add 
    path('record/mod/<int:quest_id>/<int:record_id>/', views.record_edit, name='record_mod'), # modify 
    path('record/mod/<int:quest_id>/<int:record_id>/<int:conf>', views.record_edit, name='record_mod'), # modify 
    path('record/del/<int:quest_id>/<int:record_id>/', views.record_del, name='record_del'),  # delete 
    path('issue/<int:quest_id>/<int:record_id>/', views.issue_edit, name='issue_submit'), 
    path('issue/<int:quest_id>/<int:record_id>/<int:accept>/', views.issue_edit, name='issue_submit'), 
    # About
    path('about/<str:nav>/', views.about_site, name='about'),    # List
 
]
