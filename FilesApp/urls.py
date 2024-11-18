# urls.py
from django.urls import path
from .views import FileUploadView,GenerateDownloadLinkView,DownloadFileView,FileListView,FileListView

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('download-files/<int:assignment_id>/', GenerateDownloadLinkView.as_view(), name='generate-download-link'),
    path('download-file/<str:encrypted_data>/', DownloadFileView.as_view(), name='download-file'),
    path('uploaded-files-list/', FileListView.as_view(), name='file-upload-list'),
]
