describe('Persons Page', () => {
  beforeEach(() => {
    cy.visit('/persons')
  })

  it('displays persons list', () => {
    cy.get('table').should('be.visible')
    cy.contains('Иванов').should('be.visible')
    cy.contains('Иван').should('be.visible')
    cy.contains('Иванович').should('be.visible')
  })

  it('creates a new person', () => {
    cy.contains('Создать новую персону').click()
    
    cy.get('input[placeholder="Введите фамилию"]').type('Петров')
    cy.get('input[placeholder="Введите имя"]').type('Петр')
    cy.get('input[placeholder="Введите отчество"]').type('Петрович')
    cy.get('input[placeholder="Введите email"]').type('petr@example.com')
    cy.get('input[placeholder="Введите телефон"]').type('+7 (888) 888-88-88')
    
    cy.contains('button', 'Создать').click()
    
    cy.contains('Петров').should('be.visible')
    cy.contains('Успешно').should('be.visible')
  })

  it('edits an existing person', () => {
    cy.get('button[aria-label="Открыть меню"]').first().click()
    cy.contains('Редактировать').click()
    
    cy.get('input[placeholder="Введите фамилию"]').clear().type('Сидоров')
    cy.contains('button', 'Сохранить').click()
    
    cy.contains('Сидоров').should('be.visible')
    cy.contains('Успешно').should('be.visible')
  })

  it('deletes a person', () => {
    cy.get('button[aria-label="Открыть меню"]').first().click()
    cy.contains('Удалить').click()
    
    cy.contains('Вы уверены').should('be.visible')
    cy.contains('button', 'Удалить').click()
    
    cy.contains('Успешно').should('be.visible')
  })

  it('sorts table by column', () => {
    cy.contains('button', 'Фамилия').click()
    cy.get('table tbody tr').first().should('contain', 'Иванов')
    
    cy.contains('button', 'Фамилия').click()
    cy.get('table tbody tr').first().should('contain', 'Иванов')
  })

  it('filters table by search', () => {
    cy.get('input[placeholder="Поиск по фамилии..."]').type('Иван')
    cy.get('table tbody tr').should('have.length', 1)
    cy.contains('Иванов').should('be.visible')
  })
}) 