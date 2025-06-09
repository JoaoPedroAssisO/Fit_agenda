//dashboard_cliente.js
function carregarSecao(secao) {
  let url = '';

  if (secao === 'editar') {
    url = '/usuarios/cliente/editar_perfil/';
  } else if (secao === 'agendar') {
    url = '/usuarios/cliente/agendar-treino/';
  } else if (secao === 'atividade') {
    url = '/usuarios/cliente/atividades/';
  }

  if (url) {
    fetch(url)
      .then(response => response.text())
      .then(html => {
        const conteudo = document.getElementById('conteudo-ajax');
        conteudo.innerHTML = html;
        conteudo.style.display = 'flex';

        if (secao === 'editar') {
          iniciarFormularioEdicao();
        } else if (secao === 'agendar') {
          const script = document.createElement("script");
          script.src = "/static/usuarios/js/agendar_treino_ajax.js";
          script.onload = () => {
            console.log("🟢 Script de agendar treino carregado!");
            iniciarAgendarTreino();
          };
          document.body.appendChild(script);
        } else if (secao === 'atividade') {
          const script = document.createElement("script");
          script.src = "/static/usuarios/js/atividade_cliente_ajax.js";
          script.onload = () => {
            console.log("🟢 Script de atividade carregado!");
          };
          document.body.appendChild(script);
        }
      });
  }
}

function fecharConteudo() {
  const conteudo = document.getElementById('conteudo-ajax');
  conteudo.innerHTML = '';
  conteudo.style.display = 'none';
}

function iniciarFormularioEdicao() {
  const form = document.getElementById('form-editar-perfil');
  if (!form) return;

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const formData = new FormData(form);

    fetch('/usuarios/cliente/editar_perfil/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrfToken
      },
      body: formData
    })
    .then(res => res.json())
    .then(data => {
      alert(data.mensagem);
      fecharConteudo();
    })
    .catch(() => alert('Erro ao atualizar perfil.'));
  });
}

function iniciarAgendamento() {
  if (typeof iniciarAgendarTreino === "function") {
    iniciarAgendarTreino();  // Função que estará no agendar_treino_ajax.js
  }
}

