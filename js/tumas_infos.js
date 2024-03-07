document.addEventListener("DOMContentLoaded", function() {
    const botao = document.querySelector("#btn_addturma");

    botao.addEventListener("click", function(e) {
        e.preventDefault();

        const Codigo_Turmas = document.querySelector("#Codigo").value;
        const Descricao_Turmas = document.querySelector("#Descricao").value;

        console.log(Codigo_Turmas, Descricao_Turmas);

    });
});
