from django.db import models

class Colaborador(models.Model):
    id_colaborador = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=45)
    cpf = models.CharField(max_length=45)
    
    def __str__(self):
        return self.nome

class Equipamento(models.Model):
    id_equipamento = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=90)
    # 1 para 'Disponível', 2 para 'Em Uso'
    situacao = models.IntegerField(default=1) 
    condicao = models.CharField(max_length=45)
    
    def __str__(self):
        return self.nome

class EPI(models.Model):
    id_epi = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=45)
    quantidade = models.IntegerField()
    maximo = models.IntegerField()
    
    def __str__(self):
        return self.nome

class Emprestimo(models.Model):
    id_emprestimo = models.AutoField(primary_key=True)
    data = models.DateField()
    data_devolucao = models.DateField()
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Empréstimo {self.id_emprestimo}"

class Consumo(models.Model):
    id_consumo = models.AutoField(primary_key=True)
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
    data_consumo = models.DateTimeField()
    
    def __str__(self):
        return f"Consumo {self.id_consumo}"

class Itens_Emprestimo(models.Model):
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE)
    emprestimo = models.ForeignKey(Emprestimo, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = (('equipamento', 'emprestimo'),)
        
    def __str__(self):
        return f"Item do empréstimo {self.emprestimo.id_emprestimo}"

class Consumo_EPI(models.Model):
    consumo = models.ForeignKey(Consumo, on_delete=models.CASCADE)
    epi = models.ForeignKey(EPI, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = (('consumo', 'epi'),)
        
    def __str__(self):
        return f"EPI do consumo {self.consumo.id_consumo}"