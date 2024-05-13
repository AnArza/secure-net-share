from django.urls import path
from .views import FileUploadView, FileDownloadView, FileShareView

urlpatterns = [
    path('api/files/upload/', FileUploadView.as_view(), name='file-upload'),
    path('api/files/download/<int:file_id>/', FileDownloadView.as_view(), name='file-download'),
    path('api/files/share/', FileShareView.as_view(), name='file-share'),
]
