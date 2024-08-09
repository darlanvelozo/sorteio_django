# admin.py
import csv
from django.contrib import admin
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Cliente, Configuracao
from .forms import CSVUploadForm
from django.urls import path
from django.http import HttpResponse
from io import StringIO
from .models import CSVFile, Cliente
from .forms import CSVUploadForm

@admin.register(CSVFile)
class CSVFileAdmin(admin.ModelAdmin):
    list_display = ('uploaded_at',)
    form = CSVUploadForm

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        # Processar o arquivo CSV
        csv_file = obj.file
        csv_data = csv_file.read().decode('utf-8')
        io_string = StringIO(csv_data)
        reader = csv.DictReader(io_string)
        
        for row in reader:
            Cliente.objects.create(
                id_cliente=row['id_cliente'],
                nome=row['nome'],
                numero=row['numero'],
                cpf=row['cpf'],
                ticket=row['ticket'],
                cidade=row['cidade']  
            )



class ConfiguracaoAdmin(admin.ModelAdmin):
    list_display = ('botao_ativo', 'quantidade_exibida')
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'numero', 'cpf', 'ticket', 'cidade', 'sorteado')    
    
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Configuracao, ConfiguracaoAdmin)
