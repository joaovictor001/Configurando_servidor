document.addEventListener("DOMContentLoaded", function() {
    const botao = document.querySelector("#btn_addatividade");

    botao.addEventListener("click", function(e) {
        e.preventDefault();

        const Codigo_Atividade = document.querySelector("#Codigo").value;
        const Descricao_Atividade= document.querySelector("#Descricao").value;

        console.log(Codigo_Atividade, Descricao_Atividade);

    });
});
