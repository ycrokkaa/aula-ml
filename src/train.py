import csv
import hashlib
import json
import platform
import subprocess
import sys
import uuid
from collections import Counter, defaultdict
from pathlib import Path

def ler_csv(caminho):
    with Path(caminho).open(encoding="utf-8-sig", newline="") as arquivo:
        return list(csv.DictReader(arquivo))

def salvar_json(caminho, conteudo):
    Path(caminho).write_text(
        json.dumps(conteudo, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

def sha256(caminho):
    return hashlib.sha256(Path(caminho).read_bytes()).hexdigest()

def token(texto):
    return texto.lower().split()[0]

def classe_majoritaria(contagens):
    return min(contagens, key=lambda classe: (-contagens[classe], classe))

if len(sys.argv) != 2:
    raise SystemExit("Uso: python src/train.py <model_id>")

model_id = sys.argv[1]
dataset = json.loads(Path("data/manifesto.json").read_text(encoding="utf-8-sig"))
params = json.loads(Path("params.json").read_text(encoding="utf-8-sig"))
if params != {"tokenizador": "primeira_palavra_minuscula"}:
    raise ValueError("Configuração de tokenização desconhecida.")

linhas = ler_csv("data/chamados.csv")
divisao = ler_csv("data/split.csv")
particoes = {linha["id"]: linha["particao"] for linha in divisao}
classes = ("comum", "urgente")
ids = {linha["id"] for linha in linhas}
if len(ids) != len(linhas) or len(particoes) != len(divisao) or ids != set(particoes):
    raise ValueError("IDs duplicados ou divergentes entre dataset e partição.")
if set(particoes.values()) != {"treino", "teste"}:
    raise ValueError("A partição deve conter treino e teste.")
if any(not linha["texto"].strip() or linha["classe"] not in classes for linha in linhas):
    raise ValueError("Há texto vazio ou classe inválida.")

treino = [linha for linha in linhas if particoes[linha["id"]] == "treino"]
teste = [linha for linha in linhas if particoes[linha["id"]] == "teste"]
if any({linha["classe"] for linha in grupo} != set(classes) for grupo in (treino, teste)):
    raise ValueError("As duas classes devem aparecer no treino e no teste.")

contagens = defaultdict(Counter)
for linha in treino:
    contagens[token(linha["texto"])][linha["classe"]] += 1

modelo = {
    "parametros": params,
    "entrada": "texto de chamado",
    "saida": list(classes),
    "classe_por_token": {palavra: classe_majoritaria(n) for palavra, n in contagens.items()},
    "classe_padrao": classe_majoritaria(Counter(linha["classe"] for linha in treino)),
}
Path("models").mkdir(exist_ok=True)
Path("reports").mkdir(exist_ok=True)
artefato = "models/model.json"
salvar_json(artefato, modelo)

suporte = Counter(linha["classe"] for linha in teste)
acertos = Counter()
for linha in teste:
    prevista = modelo["classe_por_token"].get(token(linha["texto"]), modelo["classe_padrao"])
    if prevista == linha["classe"]:
        acertos[linha["classe"]] += 1

avaliacao = "reports/metrics.json"
salvar_json(avaliacao, {
    "model_id": model_id,
    "dataset_id": dataset["dataset_id"],
    "protocolo": "Avaliação em partição de teste fixa",
    "split_sha256": sha256("data/split.csv"),
    "acuracia": sum(acertos.values()) / len(teste),
    "por_classe": {
        classe: {"recall": acertos[classe] / suporte[classe], "suporte": suporte[classe]}
        for classe in classes
    },
})
salvar_json("reports/modelo.json", {
    "model_id": model_id,
    "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
    "dataset_id": dataset["dataset_id"],
    "dataset_sha256": sha256("data/chamados.csv"),
    "split_sha256": sha256("data/split.csv"),
    "run_id": str(uuid.uuid4()),
    "parametros": params,
    "ambiente": {
        "python": platform.python_version(),
        "plataforma": platform.platform(),
        "dependencias_externas": [],
    },
    "artefato": artefato,
    "descritor": artefato + ".dvc",
    "artifact_sha256": sha256(artefato),
    "avaliacao": avaliacao,
})
