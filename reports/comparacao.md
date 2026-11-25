# Comparação dos modelos

## Alteração

No dataset `chamados-v2`, o chamado `006` foi corrigido de `comum` para
`urgente`. O modelo r1 e o modelo r2 foram avaliados na mesma partição de teste;
o SHA-256 de `data/split.csv` permaneceu
`1da05b6da9d900e808506b0daa36db85f317bd1ac2c7b9ee1deeeb2bc3aed850`.

## Métricas

| Modelo | Dataset | Acurácia | Recall comum | Recall urgente |
| --- | --- | ---: | ---: | ---: |
| chamados-r1 | chamados-v1 | 0,75 (3/4) | 1,00 (2/2) | 0,50 (1/2) |
| chamados-r2 | chamados-v2 | 1,00 (4/4) | 1,00 (2/2) | 1,00 (2/2) |

**Decisão: aceitar r2 para este exercício.** O recall de urgentes melhorou de
0,50 para 1,00, o recall de comuns não diminuiu e a partição de teste foi
mantida. A conclusão se aplica a este conjunto sintético e pequeno.

## Restauração de r1

A tag `modelo-r1` foi restaurada em um clone limpo. `dvc pull` recuperou os
CSVs e o modelo, e os três hashes coincidiram com `reports/modelo.json`:

| Arquivo | SHA-256 verificado |
| --- | --- |
| `data/chamados.csv` | `d03630a90bd7fc7cb1b6dfb7d8381d05e13f9669bf1146a5c3474941afb6238c` |
| `data/split.csv` | `1da05b6da9d900e808506b0daa36db85f317bd1ac2c7b9ee1deeeb2bc3aed850` |
| `models/model.json` | `72a3a67936139a3473838a6dcfa7aae1acb4c23467be1ef1056d51d485b94840` |

O commit selecionado por `modelo-r1` foi
`bfa7396b384b3b865b024a82c2de28e109fd4b84`.
