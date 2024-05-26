from model import Aluno
from tinydb import TinyDB, Query
import pandas as pd

bd = TinyDB("Alunos.json")

def inserir(model: Aluno):
    usuario = Query()
    bd.insert({
        "Nome do Aluno":model.nome,
        "Data de nascimento":model.dataNascimento,
        "CPF":model.CPF,
        "Serie":model.serie,
        "Classe":model.classe,
        "Deficiencia":model.deficiencia})
    
def mostrarTodos():
    todos = bd.all()
    return todos
    
def deletarAluno(CPF: int):
    if bd.search(Aluno.CPF==str(CPF)):
        print(bd.search)
        bd.remove(Aluno.CPF==str(CPF))
        print("Chegou aqui")
        print("Aluno deletado com Sucesso!")
    else:
        print("Aluno não encontrado")


def atualizarAluno(CPF: int, model:Aluno):
    if bd.search(Aluno.CPF==str(CPF)):
        bd.remove(Aluno.CPF==str(CPF))
        inserir(model)
    else: 
        print("Este aluno não existe")

def mostrarTabelasTodos():
    todos = pd.DataFrame(bd)
    return todos


def buscarporCPF(CPF):
    return bd.search(Aluno.CPF==str(CPF))



