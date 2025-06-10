function iniciarEditarDadosPersonal() {
  console.log("🛠️ Editar dados do personal carregado");

  const form = document.getElementById("form-editar-dados-personal");
  if (!form) {
    console.warn("⚠️ Formulário de edição de dados do personal não encontrado.");
    return;
  }

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

    console.log("📤 Enviando dados:");
    for (let [key, value] of formData.entries()) {
      console.log(`${key}: ${value}`);
    }

    fetch("/usuarios/personal/editar-dados/", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
      },
      body: formData,
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.mensagem) {
          alert("✅ " + data.mensagem);
          console.log("✅ Dados salvos com sucesso!");
          fecharConteudo();
        } else if (data.erro) {
          alert("❌ Erro: " + data.erro);
          console.error("❌ Erro retornado:", data.erro);
        }
      })
      .catch((err) => {
        alert("❌ Erro ao salvar os dados do personal.");
        console.error("❌ Erro de requisição:", err);
      });
  });
}
