from connect import inserir, mostrarTodos, deletarAluno, atualizarAluno, mostrarTabelasTodos,buscarporCPF
from model import Aluno
from flask import Flask, render_template, redirect, request, flash, session
import json
import pandas as pd 
from flask.globals import request

app = Flask (__name__)
app.config['SECRET_KEY'] = 'PI-EDUKA'

@app.route('/')
def home():
   return render_template('/loginUsuario.html')



#------------------------ Autenticação de Usuario ------------------------

@app.route('/login', methods=['POST'])
def login():

    email_login = request.form.get('email_login')
    SenhaUser = request.form.get('senha')

    with open('cadastro_professores.json') as cadastro_prof:
        listadecadastroprof = json.load(cadastro_prof)

        cont=0

        for usuario_cadastrado in listadecadastroprof:
            cont += 1

            if email_login == usuario_cadastrado['email'] and SenhaUser == usuario_cadastrado['senha']:
                
                session['UserProf_logado'] = email_login #// Manter usuario Logado entre as seções. 
                
                return redirect('/index')
            
            if cont >= len(listadecadastroprof):
                flash('Email ou senha incorretos!')
                return render_template('/loginUsuario.html')

# ------------------------------ Fim da Autenticação de Usuario ---------------------------    

@app.route('/loginUsuario', methods=['POST'])
def loginUsuario():
    return redirect('/')


@app.route('/user')
def user(): 
    return render_template('/index.html')


@app.route('/cadastrar')
def cadastrar():
    return render_template('/cadastrar.html')



# ------------------  CADASTRO DE PROFESSORES   ------------------
@app.route('/cadastroProfessor', methods=['POST'])
def cadastroProfessor():
    email = request.form.get('email_prof')
    nome = request.form.get('nome_prof')
    senha = request.form.get('senha_prof') 


    with open('cadastro_professores.json') as cadastro_prof:
        listadecadastroprof = json.load(cadastro_prof)
        
        for usuario_cadastrado in listadecadastroprof:
            if usuario_cadastrado['email'] == email:
                flash('Email já cadastrado!')
                return render_template('/loginUsuario.html')

    
    user_prof = [
        {
            "email" : email,
            "nome" : nome,
            "senha" : senha
        }
    ]

    novalista = listadecadastroprof + user_prof


    with open('cadastro_professores.json', 'w') as cadastro_prof:
        json.dump(novalista, cadastro_prof, indent=4)   


    flash(f'{nome} Usuario cadastrado com Sucesso!')
    return render_template('/loginUsuario.html')


# --------------------  FIM DA ROTA DE CADASTRO ----------------------------- 






#-------------------- CADASTRO DE ALUNOS --------------------------------------


@app.route('/index')
def index():
    result = mostrarTodos()
    return render_template('index.html',result = result)

@app.route('/CadastroAluno')
def CadastroAluno():
    return render_template('/CadastroAluno.html')

@app.route('/cadastrarAlunoBD', methods=["POST"])
def cadastrarAlunoBD():
    nome = request.form["nome"]
    dataNascimento = request.form["data_nascimento"]
    CPF = request.form["cpf"]
    serie = request.form["serie"]
    classe = request.form["classe"]
    deficiencia = request.form["deficiencia"]
    aluno = Aluno(nome,dataNascimento,CPF,serie,classe,deficiencia)
    inserir(aluno)
    return redirect('/index')

@app.route('/deletar/<int:CPF>')
def deletar(CPF):
    try:
        deletarAluno(CPF)
        return redirect('/index')
    except:
        return redirect('/')


    
@app.route('/atualizar/<int:CPF>', methods=["POST"])    
def atualizar(CPF):
    if request.method == 'POST':
        nome = request.form("nome")
        CPF = request.form("cpf")
        dataNascimento = request.form("data_nascimento")
        aluno = Aluno(CPF,nome,dataNascimento)
        try:
            atualizarAluno(CPF,aluno)
            return redirect('/index')
        except:
            return 'algo deu errado'
    else:
        aluno = buscarporCPF(CPF)
        return render_template ('Atualizar.html', aluno = aluno)
    

if __name__ in "__main__":
    app.run(debug=True)
