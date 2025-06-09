function iniciarAgendarTreino() {
  console.log("🟢 Função iniciarAgendarTreino carregada!");

  const btnVerDia = document.getElementById("ver-dia-semana");
  const inputData = document.getElementById("data");
  const selectPersonal = document.getElementById("personal");
  const horariosContainer = document.getElementById("espaco-info");

  if (!btnVerDia || !inputData || !selectPersonal || !horariosContainer) {
    console.log("⛔ Elementos do DOM não encontrados");
    return;
  }

  btnVerDia.addEventListener("click", function () {
    const dataSelecionada = inputData.value;
    const personalId = selectPersonal.value;

    if (!dataSelecionada || !personalId) {
      alert("⚠️ Selecione uma data e um personal.");
      return;
    }

    const diasSemana = ['domingo', 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado'];
    const dataObj = new Date(dataSelecionada + 'T00:00:00');  // ⚠️ Corrige fuso
    const nomeDiaSemana = diasSemana[dataObj.getDay()];

    const personalNome = selectPersonal.options[selectPersonal.selectedIndex]?.text || "Personal desconhecido";

    console.log("📅 Data:", dataSelecionada);
    console.log("👤 Personal ID:", personalId);
    console.log("👤 Personal Nome:", personalNome);
    console.log("🗓️ Dia da Semana:", nomeDiaSemana);

    fetch(`/usuarios/cliente/horarios-disponiveis/?personal_id=${personalId}&data=${dataSelecionada}`)
      .then(res => res.json())
      .then(data => {
        horariosContainer.innerHTML = "";

        if (data.horarios && data.horarios.length > 0) {
          data.horarios.forEach(horario => {
            const div = document.createElement("div");
            div.className = "time-slot";
            div.textContent = horario;
            div.dataset.valor = horario;

            div.addEventListener("click", function () {
              document.querySelectorAll(".time-slot").forEach(el => el.classList.remove("selected"));
              this.classList.add("selected");
              horariosContainer.dataset.horarioSelecionado = this.dataset.valor;
            });

            horariosContainer.appendChild(div);
          });
        } else {
          horariosContainer.innerHTML = "<p>Nenhum horário disponível.</p>";
        }
      })
      .catch(error => {
        console.error("❌ Erro ao buscar horários:", error);
      });
  });

  // Submissão do formulário
  const form = document.getElementById("form-agendar-treino");
  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const formData = new FormData(form);

    const horarioSelecionadoEl = document.querySelector(".time-slot.selected");
    const horario = horarioSelecionadoEl ? horarioSelecionadoEl.dataset.valor : "";

    if (!horario) {
      alert("⚠️ Selecione um horário antes de agendar.");
      return;
    }

    const data = formData.get("data");
    formData.append("horario", horario);

    fetch("/usuarios/cliente/agendar-treino/", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken
      },
      body: formData
    })
      .then(res => res.json())
      .then(data => {
        alert(data.mensagem);
        fecharConteudo();
      })
      .catch(() => {
        alert("❌ Erro ao enviar agendamento.");
      });
  });
}
