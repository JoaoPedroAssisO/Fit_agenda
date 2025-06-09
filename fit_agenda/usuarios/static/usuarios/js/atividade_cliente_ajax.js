document.addEventListener("click", function (e) {
  if (e.target.classList.contains("cancelar-treino")) {
    const treinoId = e.target.getAttribute("data-id");
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    if (confirm("Tem certeza que deseja cancelar este treino?")) {
      fetch("/usuarios/cliente/cancelar-treino/", {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken,
          "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `treino_id=${treinoId}`
      })
        .then(res => res.json())
        .then(data => {
          if (data.mensagem) {
            alert(data.mensagem);
            // opcional: remover ou atualizar o item cancelado na interface
            location.reload();  // ou atualize dinamicamente a linha
          } else if (data.erro) {
            alert("Erro: " + data.erro);
          }
        })
        .catch(() => alert("Erro na requisição de cancelamento."));
    }
  }
});
