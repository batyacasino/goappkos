from django.urls import path
from .views import *




urlpatterns = [
	path('', index, name='index'),
	path('add_client/', AddClient.as_view(), name='add_client_url'),
	path('detail_client/<int:pk>/', detail_client, name='detail_client_url'),
	path('detail_client/<int:pk>/upload_docs/', UploadDocs.as_view(), name='upload_docs_url'),
	path('detail_client/<int:pk>/yandex_oauth/', yandex_oauth, name='yandex_oauth_url'),
	
]

