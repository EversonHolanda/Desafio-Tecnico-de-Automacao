# Desafio QA Automation

Implementacao em Python dos fluxos do desafio: API Book Store e automacao web no DemoQA. Os cenarios usam pytest-bdd; as telas seguem Page Object Model.

## Requisitos

- Python 3.10 ou superior
- Google Chrome instalado
- Conexao com a internet para acessar `https://demoqa.com`

O Selenium Manager, incluido no Selenium 4, tenta localizar ou baixar o driver compativel com o Chrome na primeira execucao.

## Configuracao

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

No macOS/Linux, ative o ambiente com `source .venv/bin/activate`.

## Executar

```powershell
pytest
```

Por padrao, o Chrome roda em modo headless. Para acompanhar a interface, passe `--headed`:

```powershell
pytest --headed
```

Executar somente a API ou a interface:

```powershell
pytest tests/test_api_bookstore.py
pytest tests/test_ui_workflows.py
```

Os resultados Allure sao gerados automaticamente em `allure-results/` a cada execucao do pytest. Com Node.js/npm e Java 8 ou superior instalados, instale o Allure Commandline:

```powershell
npm install -g allure-commandline
```

Para visualizar o relatorio:

```powershell
allure serve allure-results
```

Para gerar um relatorio HTML permanente em `allure-report/`:

```powershell
allure generate allure-results --clean -o allure-report
allure open allure-report
```

As capturas de tela de cada teste de interface tambem sao anexadas ao respectivo resultado Allure, alem de serem salvas em `evidence/`.

Para apontar para outro ambiente DemoQA, defina `DEMOQA_BASE_URL` (por padrao, `https://demoqa.com`).

Ao final de cada teste de interface, uma captura PNG e salva em `evidence/` com data, hora e nome do teste. A pasta e ignorada pelo Git.

## Cobertura

- API: cria usuario, gera token, valida autorizacao, lista livros, seleciona dois ISBNs, aluga os livros e confirma os dados do usuario.
- Practice Form: preenche dados aleatorios, envia `tests/data/upload.txt`, valida e fecha o popup.
- Browser Windows: abre a nova janela, valida o texto e a fecha.
- Web Tables: cria, edita e remove um registro; cenario bonus cria 12 registros e remove todos.
- Progress Bar: interrompe abaixo de 25%, retoma ate 100% e reseta.
- Sortable: usa drag and drop para ordenar os elementos crescentemente.

Os testes web dependem da disponibilidade do site publico e podem ser afetados por mudancas nele ou por limitacao de requisicoes.
