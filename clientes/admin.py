import csv
from django.contrib import admin
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Cliente, Configuracao
from .forms import CSVUploadForm

def importar_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'O arquivo não é um CSV.')
                return redirect('admin:clientes_cliente_changelist')
            
            reader = csv.reader(csv_file.read().decode('utf-8').splitlines())
            for row in reader:
                Cliente.objects.create(nome=row[0], numero=row[1])
            messages.success(request, 'Clientes importados com sucesso.')
            return redirect('admin:clientes_cliente_changelist')
    else:
        form = CSVUploadForm()

    return render(request, 'admin/importar_csv.html', {'form': form})

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'numero')

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('importar-csv/', self.admin_site.admin_view(importar_csv), name='importar_csv'),
        ]
        return custom_urls + urls

class ConfiguracaoAdmin(admin.ModelAdmin):
    list_display = ('botao_ativo', 'quantidade_exibida')

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Configuracao, ConfiguracaoAdmin)
