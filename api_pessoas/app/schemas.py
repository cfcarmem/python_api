#BaseModel é a classe base para criar modelos de dados usando o Pydantic. 
# Ele fornece validação de dados, conversão automática e outras funcionalidades úteis para trabalhar
#  com dados estruturados em Python.
from pydantic import BaseModel
from datetime import date

#No Python, aqui vamos criar classes que herdam de BaseModel. Vamos definir os campos que queremos para cada modelo, e o Pydantic cuidará da validação e conversão de tipos automaticamente.

class PessoaCreate(BaseModel):
    nome: str
    nascimento: date
    login: str
    senha: str

class PessoaResponse(BaseModel):
    id_pessoa: int
    nome: str
    login: str

    