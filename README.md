# Versionamento de dados e modelos

Projeto da Atividade Prática 07: classificador de chamados com dados, modelo e
avaliações versionados com Git e DVC.

## Pré-requisitos

- Git
- Python 3.10 ou superior
- DVC 3 (`pip install "dvc>=3,<4"`)

O treino usa apenas a biblioteca padrão do Python. Execute os comandos a partir
da raiz do repositório, em Bash ou Zsh; no Windows, use o WSL. Se o comando
`dvc` não estiver no PATH, use `python -m dvc`.

## Armazenamento DVC

O remoto `storage` deste exercício usa a pasta local `dvc-storage`, irmã deste
repositório. Para restaurar os artefatos nesta máquina, mantenha essa pasta no
mesmo local e confira a configuração com:

```bash
dvc remote list
```

O caminho está definido em `.dvc/config`. Em outra máquina, configure `storage`
para apontar ao caminho local que contém os objetos DVC antes de executar
`dvc pull`:

```bash
dvc remote modify storage url "/caminho/absoluto/para/dvc-storage"
```

Esse remoto é local e não é publicado no GitHub. Portanto, quem clonar o
repositório em outra máquina também precisa receber ou configurar o
armazenamento DVC.

## Treinar

```bash
python3 src/train.py chamados-r1
python3 -m dvc add models/model.json
python3 -m dvc push models/model.json.dvc
```

As métricas e os metadados do treino são gravados em `reports/`. Registre no
Git o descritor `models/model.json.dvc` e os relatórios; o arquivo do modelo é
armazenado pelo DVC.

## Restaurar o modelo r1

Clone o repositório em uma pasta irmã de `dvc-storage`, selecione a tag r1 e
recupere os arquivos DVC:

```bash
git clone URL_DO_REPOSITORIO aula-ml-restauracao
cd aula-ml-restauracao
git switch --detach modelo-r1
python3 -m dvc remote list
python3 -m dvc pull
```

Confira os hashes restaurados comparando-os aos registrados em
`reports/modelo.json`:

```bash
python3 - <<'PY'
import hashlib
import json
from pathlib import Path

manifesto = json.loads(Path("reports/modelo.json").read_text(encoding="utf-8"))
for caminho, campo in [
    ("data/chamados.csv", "dataset_sha256"),
    ("data/split.csv", "split_sha256"),
    ("models/model.json", "artifact_sha256"),
]:
    obtido = hashlib.sha256(Path(caminho).read_bytes()).hexdigest()
    if obtido != manifesto[campo]:
        raise SystemExit(f"Hash divergente para {caminho}")
    print(f"OK {caminho} {obtido}")
PY
```

Os resultados da comparação entre r1 e r2 e os hashes verificados na
restauração estão em [reports/comparacao.md](reports/comparacao.md).
