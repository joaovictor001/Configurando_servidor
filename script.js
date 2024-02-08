

document.addEventListener('DOMContentLoaded', function() {

    const button = document.querySelector('#button');
    const tabelaCorpo = document.querySelector('#tabela-corpo');

    
        button.addEventListener('click', function() {
            const data = document.querySelector("#data");
            const aula = document.querySelector("#Aula")
            const Conteudo = document.querySelector("#Cont")
            const Dificult = document.querySelector("#Dificult")

    
            const newRow = document.createElement('tr');
            const newData = document.createElement('td');
            newData.textContent = new Date();
            newRow.appendChild(newData);

            const newAula = document.createElement('td');
            newAula.textContent = aula.value;
            newRow.appendChild(newAula);

            const newConteudo = document.createElement('td');
            newConteudo.textContent = Conteudo.value;
            newRow.appendChild(newConteudo);

            const newDificuldade = document.createElement('td');
            newDificuldade.textContent = "⭐" * Dificult;
            newRow.appendChild(newDificuldade);

            const newButton = document.createElement('td');
            const newButtonElement = document.createElement('button');
            newButtonElement.textContent = 'Página da aula';
            newButtonElement.classList.add('editar-btn');
            newButton.appendChild(newButtonElement);
            newRow.appendChild(newButton);

            tabelaCorpo.appendChild(newRow);

            // Limpar campos de input após adicionar nova linha
            data.value = '';
            aula.value = '';
            Conteudo.value = '';
            Dificult.value = '';
            
            
    });
});


