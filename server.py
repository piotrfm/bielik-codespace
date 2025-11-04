import os
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# ↓↓↓ PODMIEŃ na właściwy ID Bielika z HF, gdy jest dostępny
MODEL_ID = os.environ.get("MODEL_ID", "HuggingFaceH4/zephyr-7b-beta")  # placeholder

app = FastAPI(title="Bielik (CPU) – demo API")

print("⏳ Loading tokenizer/model (CPU)…")
tok = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float32,
    device_map="cpu"
)
print("✅ Model loaded")

class Inp(BaseModel):
    prompt: str
    max_new_tokens: int = 64
    temperature: float = 0.2

@app.post("/generate")
def generate(inp: Inp):
    inputs = tok(inp.prompt, return_tensors="pt")
    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=inp.max_new_tokens,
            do_sample=inp.temperature > 0,
            temperature=inp.temperature
        )
    text = tok.decode(out[0], skip_special_tokens=True)
    return {"output": text}
