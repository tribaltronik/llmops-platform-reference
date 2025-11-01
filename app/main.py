from fastapi import FastAPI
from pydantic import BaseModel
from vllm import LLM, SamplingParams

# --- Configuração ---
# Modelo pequeno e rápido para testes
MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0" 

# Configuração do vLLM. 'gpu_memory_utilization' é chave no K8s
llm = LLM(
    model=MODEL_NAME,
    trust_remote_code=True,
    gpu_memory_utilization=0.85 # Tenta usar até 85% da VRAM disponível
)

# Parâmetros de amostragem (pode ser configurado via API)
SAMPLING_PARAMS = SamplingParams(
    temperature=0.7, 
    top_p=0.95, 
    max_tokens=256
)

app = FastAPI(title="TinyLlama K8s Service")

# Modelo Pydantic para a requisição de inferência
class InferenceRequest(BaseModel):
    prompt: str
    
# --------------------

@app.get("/health")
def health_check():
    """Endpoint de health check simples."""
    return {"status": "ok", "model": MODEL_NAME}

@app.post("/generate")
def generate_text(request: InferenceRequest):
    """Endpoint principal para gerar texto."""
    
    # Faz a inferência usando o vLLM
    outputs = llm.generate([request.prompt], SAMPLING_PARAMS)
    
    # Extrai o texto gerado do output
    generated_text = outputs[0].outputs[0].text.strip()
    
    # Retorna o resultado
    return {
        "prompt": request.prompt,
        "response": generated_text,
        "tokens": len(outputs[0].outputs[0].token_ids)
    }