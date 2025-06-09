function iniciarEditarDadosPersonal() {
  console.log("🛠️ Editar dados do personal carregado");

  const form = document.getElementById("form-editar-personal");
  if (!form) return;

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const formData = new FormData(form);

    // Coleta as especialidades marcadas
    const especialidades = [];
    document.querySelectorAll("input[name='especialidades']:checked").forEach((el) => {
      especialidades.push(el.value);
    });

    formData.append("especialidades_ids", especialidades.join(","));

    fetch("/usuarios/personal/editar-dados/", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
      },
      body: formData,
    })
      .then((res) => res.json())
      .then((data) => {
        alert(data.mensagem);
        fecharConteudo();
      })
      .catch(() => {
        alert("Erro ao salvar os dados do personal.");
      });
  });
}