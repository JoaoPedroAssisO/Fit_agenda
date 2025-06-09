/*/document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("form-editar-perfil");

    form.addEventListener("submit", function (event) {
        event.preventDefault();

        const formData = new FormData(form);

        fetch(form.action || window.location.href, {
            method: "POST",
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        })
            .then(response => {
                if (!response.ok) throw new Error("Erro na resposta do servidor.");
                return response.text();
            })
            .then(html => {
                // Substitui o conteúdo do modal com a resposta (pode conter erros de validação ou sucesso)
                document.getElementById("conteudo-dinamico").innerHTML = html;

                // Reexecuta o script para manter os eventos funcionando após re-renderizar o HTML
                const script = document.createElement("script");
                script.src = "/static/js/editar_perfil.js";
                document.body.appendChild(script);
            })
            .catch(error => {
                alert("Erro ao salvar: " + error.message);
            });
    });
});*/
