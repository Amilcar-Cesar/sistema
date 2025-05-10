import sqlite3
from sqlite3 import Error
import time
# Criando/conectando ao banco de dados

banco = sqlite3.connect('Banco_de_dados.db')
cursor = banco.cursor()

# Criar a tabela usuários
cursor.execute("""
CREATE TABLE IF NOT EXISTS Login (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    nome TEXT NOT NULL CHECK(length(trim(nome)) > 0), 
    login TEXT UNIQUE NOT NULL CHECK(length(trim(login)) > 0), 
    senha TEXT NOT NULL CHECK(length(trim(senha)) > 0)
)
""")
banco.commit()

# cria tabela de especialidades
cursor.execute("""
CREATE TABLE IF NOT EXISTS Especialidades ( 
        especialidade TEXT UNIQUE NOT NULL CHECK(length(trim(especialidade)) > 0)
) 
""")
banco.commit()

# criação da função especialidades


def cad_espec():
    while True:
        print('\n_____Cadastro de Especialidades_____')
        espec = input("Digite a especialidade: ")

        if not espec:
            print("Erro: A especialidade não pode estar vazia!")
            continue

        try:
            cursor.execute(
                "INSERT INTO Especialidades (especialidade) VALUES (?)", (espec,))
            banco.commit()
            print("Especialidade cadastrada com sucesso!")

        except sqlite3.IntegrityError as e:
            if "UNIQUE" in str(e):
                print(f"Erro, a especialidade {espec} já existe.")
            else:
                print(f"Erro de integridade: {e}")

        except sqlite3.Error as e:
            print(f"Erro no banco de dados: {e}")

        except Exception as e:
            print(f"Erro inesperado: {e}")

        print('-'*50)
        resp = input(
            "Gostaria de criar outra especialidade? (S/N)  ").strip().upper()
        if resp != "S":
            break
        print('-'*50)


cad_espec()

# loop para adição de usuários


def cad_usuario():
    while True:

        nome = input("NOME: ")
        login = input("LOGIN: ")
        senha = input("SENHA: ")

        try:
            cursor.execute("INSERT INTO Login (nome, login, senha) VALUES (?, ?, ?)",
                           (nome, login, senha))
            banco.commit()
            print("Usuário cadastrado com sucesso!")

        except sqlite3.IntegrityError as e:
            if "UNIQUE" in str(e):
                print("ERRO: Este login já está em uso. Escolha outro.")
            else:
                print(f"Erro no cadastro: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")

        print('-'*50)
        resp = input(
            "Gostaria de criar outro usuário? (S/N)  ").strip().upper()
        if resp != "S":
            break
        print('-'*50)

    # Fechando a conexão
    banco.close()
    time.sleep(1)
    print("Usuário criado com sucesso!")

# cad_usuario()


def menu():
    while True:
        opcao = int(input("""
        Selecione abaixo qual tarefa deseja realizar: 
        1 - Selecionar todos os dados da tabela
        2 - Selecionar por idade
        3 - Mostre o total de clientes cadastrados
        4 - Cadastrar cliente
        5 - Atualizar um email
        51 - Aumente a idade de todos os clientes em 1
        52 - Deletar um cliente
        """))

        # criar função
        if opcao == 1:
            cursor.execute("SELECT * FROM clientes")
            print(cursor.fetchall())
            banco.close()
            break
        # criar função
        if opcao == 2:
            cursor.execute(
                "SELECT nome, idade FROM CLIENTES WHERE idade >= 24")
            print(cursor.fetchall())
            banco.close()
            break
        # criar função
        if opcao == 3:
            cursor.execute("SELECT nome, idade FROM clientes WHERE idade < 20")
            total = cursor.fetchall()
            print(total)
            break

        if opcao == 4:
            cadastro()

        if opcao == 5:
            id_cliente = int(input("Informe o ID do cliente: "))
            email_novo = input("Digite o novo email que deseja atualizar: ")
            cursor.execute(
                "UPDATE clientes SET email = ? WHERE id = ?", (email_novo, id_cliente))
            banco.commit()
            time.sleep(1)
            print("Email atualizado com sucesso!")
            break

        if opcao == 51:
            cursor.execute("UPDATE clientes SET idade = idade + 1")
            banco.commit()
            time.sleep(1)
            print("Idade atualizada com sucesso!")
            break

        if opcao == 52:
            delete_cliente = int(
                input("Informe o ID do cliente que deseja remover: "))
            # nao consegui definir uma concatenação para definir qual ID sera deletado
            cursor.execute("DELETE FROM clientes WHERE id = ?")
            banco.commit()
            time.sleep(1)
            print("Cliente deletado com sucesso!")
            break
