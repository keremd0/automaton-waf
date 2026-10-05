import json
import httpx
from urllib.parse import unquote_plus
from fastapi import FastAPI, Request, Response
from core.dfa_engine import DFAMachine
from core.tokenizer import tokenize

app = FastAPI(title="Automaton WAF")

with open("config/rules.json", "r") as f:
    config = json.load(f)

transitions = {(t["from"], t["token"]): t["to"] for t in config["transitions"]}
dfa = DFAMachine(transitions, config["initial_state"], set(config["accept_states"]))

BACKEND_URL = "http://127.0.0.1:5000"

def is_malicious(text: str) -> bool:
    if not text:
        return False
    decoded = unquote_plus(text)
    tokens = tokenize(decoded)
    matched = dfa.process(tokens)
    print(f"\n[WAF LOG] Incelenen Metin: {decoded}", flush=True)
    print(f"[WAF LOG] Token Akisi: {tokens}", flush=True)
    print(f"[WAF LOG] Saldiri Tespiti: {matched}\n", flush=True)
    return matched

@app.middleware("http")
async def waf_inspection_middleware(request: Request, call_next):
    # 1. URL ve Query String Analizi
    full_url = str(request.url)
    if is_malicious(full_url):
        return Response(content="[!] WAF: Saldiri tespit edildi, gecemezsin!\n", status_code=403)

    # 2. Gövde (Body) Analizi
    body = await request.body()
    body_text = body.decode("utf-8", errors="ignore")
    if body_text and is_malicious(body_text):
        return Response(content="[!] WAF: Saldiri tespit edildi, gecemezsin!\n", status_code=403)

    # 3. Temizse backend'e ilet
    async with httpx.AsyncClient() as client:
        backend_url = f"{BACKEND_URL}{request.url.path}"
        resp = await client.request(
            method=request.method,
            url=backend_url,
            headers=request.headers.raw,
            content=body,
            params=request.query_params
        )
        return Response(content=resp.content, status_code=resp.status_code)
