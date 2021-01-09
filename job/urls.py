from django.contrib import admin
from django.urls import path
from . import views



app_name="jobs"

urlpatterns = [
    path('dashboard/',views.dashboard,name = "dashboard"),
    path('addjob/',views.addJob,name = "addjob"),
    path('job/<int:id>',views.detail,name = "detail"),
    path('update/<int:id>',views.updateJob,name = "update"),
    path('delete/<int:id>',views.deleteJob,name = "delete"),
    path('',views.jobs,name = "jobs"),
    path('comment/<int:id>',views.addComment,name = "comment"),
    
     
]