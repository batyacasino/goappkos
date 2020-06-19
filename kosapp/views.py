from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import *
from django.views.generic import View
from django.core.files.storage import FileSystemStorage

from .forms import *

def index(request):
	clients = Client.objects.all()
	clients_list = []
	for client in clients:
		email_count = app.email_counters(client.email[:-15])
		client_dict = {
			'id': client.id,
			'claimant': client.claimant,
			'defendant': client.defendant,
			'email_count': email_count['unread']
		}
		clients_list.append(client_dict)
	return render(request, 'kosapp/index.html', {"clients": clients_list})


def detail_client(request, pk):
	client = Client.objects.get(id=pk)
	email_count = app.email_counters(client.email[:-15])
	files = ClientDocs.objects.filter(client_id=pk)
	return render(request, 'kosapp/detail_client.html', {
													"client": client, 
													"files": files,
													'email_count':email_count,
												})
def yandex_oauth(request, pk):
	client = Client.objects.get(id=pk)
	link = app.passport_oauth('https://mail.yandex.ru/', email=client.email)
	return render(request, 'kosapp/yandex_oauth.html', {'link':link[1:]})





class AddClient(View):
	def get(self, request):
		form = ClientForm()
		return render(request, 'kosapp/add_client.html', {"form": form})

	def post(self, request):
		bound_form = ClientForm(request.POST)
		if bound_form.is_valid():
			new_client = bound_form.save()
			return render(request, 'kosapp/detail_client.html', {"client": new_client,})			
		return render(request, 'kosapp/add_client.html', {"form": bound_form})


class UploadDocs(View):
	def get(self, request, pk):
		client = Client.objects.get(id=pk)
		form = UploadDocsForm()
		return render(request, 'kosapp/upload_docs.html', {"form": form, "client": client})

	def post(self, request, pk):
		client = Client.objects.get(id=pk)
		bound_form = UploadDocsForm(request.POST, request.FILES)
		if bound_form.is_valid():
			new_file = bound_form.save()
			files = ClientDocs.objects.filter(client_id=pk)
			return render(request, 'kosapp/detail_client.html', {"client": client, "files": files})			
		return render(request, 'kosapp/upload_docs.html', {"form": bound_form, "client": client})


def alldelete(request):
	clients = Client.objects.all()
	clients.delete()
	return render(request, 'kosapp/index.html', {"clients": clients,})
