# Relatorio de Apresentacao: Desafio de Automacao QA

## Objetivo

Este projeto automatiza fluxos da API Book Store e da interface web DemoQA. O objetivo e validar jornadas funcionais de ponta a ponta e produzir evidencias que facilitem a analise dos resultados.

## Roteiro de fala

> Olá. Vou apresentar minha solução para o desafio de automação QA. O projeto valida funcionalidades da API Book Store e de diferentes áreas da aplicação web DemoQA.
>
> Para estruturar os testes, usei Python com pytest e pytest-bdd. Os cenários ficam descritos em arquivos Gherkin, no formato Dado, Quando e Então, e as interações com a interface foram organizadas com Page Object Model. Para a automação web, usei Selenium; para as chamadas HTTP, a biblioteca Requests. Os resultados e as evidências são registrados com Allure.
>
> Na API, o teste cria um usuário com credenciais geradas para a execução, solicita um token, confirma a autorização, consulta o catálogo, seleciona dois livros e verifica se eles aparecem na coleção do usuário.
>
> Na interface, os testes cobrem o envio do formulário com upload de arquivo, a abertura e o fechamento de uma nova janela, as operações de criação, edição e exclusão em Web Tables, a inclusão e remoção em lote de doze registros, o controle da barra de progresso e a ordenação de itens por arrastar e soltar.
>
> Na execução representada pelo relatório Allure que está no projeto, os sete cenários foram aprovados: um de API e seis de interface, sem falhas ou testes ignorados. Além do resultado, as capturas de tela dos testes web são salvas como evidência e anexadas ao Allure.
>
> Como o alvo é o DemoQA público, a execução depende de conexão com a internet e pode ser afetada por indisponibilidade ou mudanças no site. Portanto, o resultado apresentado comprova essa execução específica, não garante que execuções futuras terão o mesmo resultado.
>
> Como próximos passos, eu ampliaria a cobertura com cenários negativos e validações de erro, e executaria os testes em mais de um navegador ou em uma pipeline de CI. Obrigado.

## Escopo automatizado

| Área | Validações |
| --- | --- |
| Book Store API | Criação de usuário, geração de token, autorização, consulta do catálogo, empréstimo de dois livros e conferência da coleção. |
| Practice Form | Preenchimento e envio do formulário com upload de arquivo; validação e fechamento da confirmação. |
| Browser Windows | Abertura de uma nova janela, validação do texto esperado e fechamento. |
| Web Tables | Criação, edição e exclusão de um registro; criação e remoção de doze registros. |
| Progress Bar | Interrupção antes de 25%, conclusão até 100% e reset para zero. |
| Sortable | Ordenação crescente dos itens por drag and drop. |

## Tecnologias e organização

- Python 3.10 ou superior, pytest e pytest-bdd.
- Selenium para os fluxos web e Requests para a API.
- Page Object Model para concentrar as interações com as páginas.
- Allure para visualização dos resultados e anexos.
- Cenários BDD em `features/`, implementações de teste em `tests/` e componentes de automação em `qa_automation/`.

## Resultado registrado

O relatório Allure atualmente presente no projeto registra **7 testes aprovados, 0 falhas, 0 testes interrompidos e 0 ignorados**. Esse número se refere à execução armazenada no relatório; uma nova execução pode apresentar resultados diferentes por depender do serviço público.

Os testes são executados por padrão em modo headless. Para acompanhar a interface durante uma demonstração:

```powershell
pytest --headed
```

Para abrir o relatório Allure após a execução, com o Allure Commandline instalado:

```powershell
allure serve allure-results
```

## Pontos de atenção e evolução

- Os cenários web dependem da disponibilidade e da estrutura atual do DemoQA.
- A execução requer Chrome, conexão com a internet e as dependências instaladas.
- O foco implementado é a validação funcional dos fluxos descritos; cenários negativos, compatibilidade entre navegadores e execução em CI podem ser incrementados em etapas futuras.
