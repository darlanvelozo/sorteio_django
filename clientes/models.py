from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    numero = models.CharField(max_length=20)
    sorteado = models.BooleanField(default=False)  # Campo para marcar os sorteados

    def __str__(self):
        return self.nome
class Configuracao(models.Model):
    botao_ativo = models.BooleanField(default=False)
    quantidade_exibida = models.IntegerField(default=0)

    def __str__(self):
        return f'Configuração ({self.id})'
