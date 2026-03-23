# Integracao de IA

Este projeto agora pode gerar um diagnostico automatico da execucao em `relatorio_ia.md`.

## Como ativar

Defina estas variaveis de ambiente:

- `AI_API_KEY`: chave da API.
- `AI_API_URL`: endpoint compativel com `chat/completions`.
- `AI_MODEL`: modelo a usar.
- `AI_ENABLED`: use `false`, `0` ou `off` para desligar.

## Comportamento

- A playlist continua sendo gerada normalmente.
- No final da execucao, o script resume sucessos, bloqueios e canais offline.
- Se a chave da IA estiver configurada, esse resumo e enviado para a API e o retorno e salvo em `relatorio_ia.md`.

## Exemplo de configuracao

```powershell
$env:AI_API_KEY="sua-chave"
$env:AI_MODEL="gpt-4o-mini"
python gerar_m3u8.py
```
