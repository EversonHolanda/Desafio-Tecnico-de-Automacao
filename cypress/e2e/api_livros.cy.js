describe('Desafio QA - API Loja de Livros', () => {
  
  // Criando sufixo aleatório para garantir que o usuário seja sempre único a cada execução
  const numeroAleatorio = Math.floor(Math.random() * 99999);
  const nomeUsuario = `qa_candidato_${numeroAleatorio}`;
  const senhaUsuario = `Teste@123${numeroAleatorio}`;
  
  let idDoUsuario = '';
  let tokenAcesso = '';
  let listaIsbns = [];

  it('deve executar o fluxo completo de ponta a ponta na API', () => {
    
    // 1. Cadastrar um novo usuário no sistema
    cy.request({
      method: 'POST',
      url: 'https://demoqa.com/Account/v1/User',
      body: {
        userName: nomeUsuario,
        password: senhaUsuario
      }
    }).then((respostaCriacao) => {
      expect(respostaCriacao.status).to.eq(201);
      idDoUsuario = respostaCriacao.body.userID;
    });

    // 2. Gerar o token de autenticação para o usuário recém-criado
    cy.request({
      method: 'POST',
      url: 'https://demoqa.com/Account/v1/GenerateToken',
      body: {
        userName: nomeUsuario,
        password: senhaUsuario
      }
    }).then((respostaToken) => {
      expect(respostaToken.status).to.eq(200);
      expect(respostaToken.body.status).to.eq('Success');
      tokenAcesso = respostaToken.body.token;
    });

    // 3. Validar se o usuário realmente consta como autorizado
    cy.request({
      method: 'POST',
      url: 'https://demoqa.com/Account/v1/Authorized',
      body: {
        userName: nomeUsuario,
        password: senhaUsuario
      }
    }).then((respostaAuth) => {
      expect(respostaAuth.status).to.eq(200);
      expect(respostaAuth.body).to.be.true;
    });

    // 4. Buscar a lista de livros disponíveis na loja de livros e capturar os dois primeiros
    cy.request({
      method: 'GET',
      url: 'https://demoqa.com/BookStore/v1/Books'
    }).then((respostaLivros) => {
      expect(respostaLivros.status).to.eq(200);
      
      // Pega os dois primeiros livros da listagem geral
      listaIsbns.push(respostaLivros.body.books[0].isbn);
      listaIsbns.push(respostaLivros.body.books[1].isbn);

      // 5. Realizar o aluguel dos livros utilizando o token de autorização
      cy.request({
        method: 'POST',
        url: 'https://demoqa.com/BookStore/v1/Books',
        headers: {
          Authorization: `Bearer ${tokenAcesso}`
        },
        body: {
          userId: idDoUsuario,
          collectionOfIsbns: [
            { isbn: listaIsbns[0] },
            { isbn: listaIsbns[1] }
          ]
        }
      }).then((respostaAluguel) => {
        expect(respostaAluguel.status).to.eq(201);

        // 6. Conferir se os livros alugados aparecem corretamente no perfil do usuário
        cy.request({
          method: 'GET',
          url: `https://demoqa.com/Account/v1/User/${idDoUsuario}`,
          headers: {
            Authorization: `Bearer ${tokenAcesso}`
          }
        }).then((respostaDetalhes) => {
          expect(respostaDetalhes.status).to.eq(200);
          expect(respostaDetalhes.body.books).to.have.length(2);
        });
      });
    });
  });
});