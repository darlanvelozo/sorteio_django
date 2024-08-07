import csv
from django.shortcuts import render, redirect
from django.contrib import messages
import random
from .models import Cliente, Configuracao  # Certifique-se de que Configuracao está importado
def upload_csv(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            csv_file = request.FILES['file']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'O arquivo não é um CSV.')
                return redirect('clientes:upload_csv')
          
            reader = csv.reader(csv_file.read().decode('utf-8').splitlines())
            for row in reader:
                # Ignorar a primeira linha se contiver cabeçalhos
                if reader.line_num == 1:
                    continue
                Cliente.objects.create(nome=row[0], numero=row[1])
            messages.success(request, 'Clientes importados com sucesso.')
        else:
            messages.error(request, 'Nenhum arquivo foi selecionado.')
        
        return redirect('clientes:upload_csv')
    
    return render(request, 'clientes/upload_csv.html')
def lista_clientes(request):
    configuracao = Configuracao.objects.first()
    
    if request.method == 'POST':
        if configuracao and configuracao.botao_ativo:
            quantidade_exibida = configuracao.quantidade_exibida
            clientes = Cliente.objects.order_by('?')[:quantidade_exibida]  # Ordena aleatoriamente e limita a quantidade
        else:
            clientes = Cliente.objects.none()
    else:
        clientes = []

    context = {
        'clientes': clientes,
        'botao_ativo': configuracao.botao_ativo if configuracao else False
    }
    return render(request, 'clientes/lista_clientes.html', context)