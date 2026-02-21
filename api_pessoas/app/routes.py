
from datetime import date
from fastapi import APIRouter,UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from .db import get_conn
from .schemas import PessoaCreate
import os
import shutil
import hashlib


router = APIRouter()
UPLOAD_DIR = 'upload'
os.makedirs(UPLOAD_DIR, exist_ok=True)

#rota de teste
#@router.get("/health/db")
# def health_db():
#     try:
#         with get_conn() as conn:
#             with conn.cursor() as cur:
#                 cur.execute("SELECT now();")
#                 return {"status": "ok", "db_time": cur.fetchone()[0]}
#     except Exception as e:
#         return {"status": "error", "message": str(e)}


@router.post("/pessoas")
def criar_pessoa(
    nome: str = Form(...),
    nascimento: date = Form(...),
    login: str = Form(...),
    senha: str = Form(...),
    file: UploadFile = File(...)
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Somente PDF é permitido")
    senha_md5 = hash_md5(senha)
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:

                # insere pessoa
                cur.execute(
                    """
                    INSERT INTO pessoa (nome, nascimento, login, senha)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id_pessoa
                    """,
                    (nome, nascimento, login, senha_md5)
                )

                id_pessoa = cur.fetchone()[0]

                # salva arquivo no disco
                filename = f"{id_pessoa}_{file.filename}"
                path = os.path.join(UPLOAD_DIR, filename)

                with open(path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)

                # insere registro do arquivo
                cur.execute(
                    """
                    INSERT INTO arquivos (id_pessoa, path)
                    VALUES (%s, %s)
                    """,
                    (id_pessoa, path)
                )

        return {
            "id_pessoa": id_pessoa,
            "mensagem": "Pessoa criada com arquivo PDF"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/pessoas")
def listar_pessoas():
   sql = "Select a.id_pessoa, a.nome, a.login, a.nascimento, b.path from pessoa a" \
   " left join arquivos b on a.id_pessoa = b.id_pessoa"
   with get_conn() as conn:
       with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()
       
   
@router.get("/pessoas/{id_pessoa}/documento")
def baixar_documento(id_pessoa: int):
    sql = """
        SELECT path
        FROM arquivos
        WHERE id_pessoa = %s
        ORDER BY id_arquivo DESC
        LIMIT 1
    """

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (id_pessoa,))
            row = cur.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Documento não encontrado")

    path = row[0]

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Arquivo não existe no servidor")

    return FileResponse(
        path,
        media_type="application/pdf",
        filename=os.path.basename(path)
    )

@router.put("/pessoas/{id_pessoa}")
def atualizar_pessoa(
    id_pessoa: int,
    nome: str | None = Form(None),
    nascimento: date | None = Form(None),
    login: str | None = Form(None),
    senha: str | None = Form(None),
):
    campos = []
    valores = []

    if nome is not None:
        campos.append("nome = %s")
        valores.append(nome)

    if nascimento is not None:
        campos.append("nascimento = %s")
        valores.append(nascimento)

    if login is not None:
        campos.append("login = %s")
        valores.append(login)

    if senha is not None:
        campos.append("senha = %s")
        valores.append(hash_md5(senha))

    if not campos:
        raise HTTPException(
            status_code=400,
            detail="Nenhum campo informado para atualização"
        )

    sql = f"""
        UPDATE pessoa
        SET {", ".join(campos)}
        WHERE id_pessoa = %s
    """

    valores.append(id_pessoa)

    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, valores)

                if cur.rowcount == 0:
                    raise HTTPException(
                        status_code=404,
                        detail="Pessoa não encontrada"
                    )

        return {"mensagem": "Pessoa atualizada com sucesso"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

def hash_md5(senha: str) -> str:
    return hashlib.md5(senha.encode("utf-8")).hexdigest()