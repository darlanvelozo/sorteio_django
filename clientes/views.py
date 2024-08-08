import csv
from django.shortcuts import render, redirect
from django.contrib import messages
import random
from .models import Cliente, Configuracao  # Certifique-se de que Configuracao está importado
from .forms import CSVUploadForm
from io import StringIO
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test


def admin_required(user):
    return user.is_superuser

@user_passes_test(admin_required, login_url='/admin/login/')
def lista_clientes(request):
    configuracao = Configuracao.objects.first()
    
    if request.method == 'POST' and configuracao and configuracao.botao_ativo:
        quantidade_exibida = configuracao.quantidade_exibida

        # Resetar o status de sorteio de todos os clientes
        Cliente.objects.all().update(sorteado=False)

        # Selecionar novos clientes sorteados
        clientes_sorteados = Cliente.objects.order_by('?')[:quantidade_exibida]
        
        # Atualizar o status de sorteio dos novos sorteados
        Cliente.objects.filter(id__in=[cliente.id for cliente in clientes_sorteados]).update(sorteado=True)
    else:
        # Se não houver sorteio, mostrar todos os clientes sorteados
        clientes_sorteados = Cliente.objects.filter(sorteado=True)

    context = {
        'clientes': clientes_sorteados,
        'botao_ativo': configuracao.botao_ativo if configuracao else False
    }
    return render(request, 'clientes/lista_clientes.html', context)

def home_page(request):
    form = CPFForm()
    ganhadores = Cliente.objects.filter(sorteado=True)
    return render(request, 'clientes/home_page.html', {'form': form, 'ganhadores': ganhadores})

def home(request):
    cpf_query = request.GET.get('cpf', '')
    clientes = Cliente.objects.filter(cpf=cpf_query) if cpf_query else []
    ganhadores = Cliente.objects.filter(sorteado=True)

    return render(request, 'clientes/home.html', {
        'clientes': clientes,
        'cpf_query': cpf_query,
        'ganhadores': ganhadores,
    })