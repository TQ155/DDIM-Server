from django.urls import path
from . import views

urlpatterns = [
    path("files/", views.UploadedFilesList.as_view()),
    path('files/<int:pk>/', views.UploadedFilesObj.as_view()),
    path("filemeta/", views.FileMetadataList.as_view()),
    path('filemeta/<int:pk>/', views.FileMetadataObj.as_view()),
    path('createrule/', views.CreateRuleList.as_view()),
    path('createrule/<int:pk>/', views.CreateRuleObj.as_view()),
]