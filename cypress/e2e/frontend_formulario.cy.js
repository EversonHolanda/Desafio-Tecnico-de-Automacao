describe('Desafio QA - Automação de Frontend Formulários QA - Automação de Frontend na Loja de Livros', () => {

  beforeEach(() => {
    cy.visit('https://demoqa.com/automation-practice-form');
    cy.viewport(1280, 720);
  });

  it('deve preencher o formulário de cadastro de usuário e anexar arquivo com sucesso', () => {

    // Dados para preenchimento
    const primeiroNome = 'Everson';
    const sobrenome = 'Holanda';
    const emailUsuario = 'everson.qa@teste.com';
    const numeroCelular = '11988887777';

    // 1. Preencher informações pessoais
    cy.get('#firstName').should('be.visible').type(primeiroNome);
    cy.get('#lastName').type(sobrenome);
    cy.get('#userEmail').type(emailUsuario);

    // 2. Selecionar o gênero
    cy.get('label[for="gender-radio-1"]').click();

    // 3. Preencher o telefone móvel
    cy.get('#userNumber').type(numeroCelular);

    // 4. Selecionar Hobbies
    cy.get('label[for="hobbies-checkbox-1"]').click(); // Sports
    cy.get('label[for="hobbies-checkbox-2"]').click(); // Reading

    // 5. Fazer upload do arquivo TXT armazenado na pasta fixtures
    cy.get('#uploadPicture').selectFile('cypress/fixtures/teste.txt');

    // 6. Inserir endereço atual
    cy.get('#currentAddress').type('Rua de Testes de Automação - São Paulo, SP');

    // 7. Submeter o formulário
    cy.get('#submit').click({ force: true });

    // 8. Validar se o modal de confirmação do envio apareceu na tela
    cy.get('.modal-content').should('be.visible');
    cy.get('#example-modal-sizes-title-lg').should('have.text', 'Thanks for submitting the form');

    // 9. Validar que o nome do arquivo anexado aparece no resumo do modal
    cy.get('.table-responsive').should('contain', 'teste.txt');

    // 10. Fechar o modal
    cy.get('#closeLargeModal').click({ force: true });
  });

});