# Imagem base otimizada para CUDA (necessária para GPUs e vLLM)
FROM nvidia/cuda:12.1.1-devel-ubuntu22.04

# Instalação de dependências do sistema
RUN apt-get update && apt-get install -y \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Configuração do ambiente Python
WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY app/ .

# Expõe a porta que o Uvicorn vai usar
EXPOSE 8000

# Comando para iniciar o serviço
# O Uvicorn roda o FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]