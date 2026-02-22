FROM python:3.11-slim

# diretório dentro do container
WORKDIR /app

# copia dependências
COPY requirements.txt .

# instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# copia o código
COPY . .

# expõe a porta da API
EXPOSE 8000

# comando que sobe a API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]