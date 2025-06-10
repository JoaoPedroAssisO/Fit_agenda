function carregarSecao(secao) {
  console.log("🔁 carregarSecao chamada com:", secao);

  let url = '';
  let scriptUrl = '';
  let initFunction = null;

  if (secao === 'editar_personal') {
    url = '/usuarios/personal/editar_perfil/';
    scriptUrl = '/static/usuarios/js/editar_perfil_personal_ajax.js';
    initFunction = 'iniciarFormularioEdicaoPersonal';
  } else if (secao === 'editar_dados') {
    url = '/usuarios/personal/editar-dados-form/';
    scriptUrl = '/static/usuarios/js/editar_dados_personal_ajax.js';
    initFunction = 'iniciarEditarDadosPersonal';
  }

  if (url) {
    fetch(url)
      .then(response => response.text())
      .then(html => {
        const conteudo = document.getElementById('conteudo-ajax');
        conteudo.innerHTML = html;
        conteudo.style.display = 'flex';

        const script = document.createElement("script");
        script.src = scriptUrl;
        script.onload = () => {
          console.log("✅ Script carregado:", scriptUrl);
          if (typeof window[initFunction] === 'function') {
            window[initFunction]();
          } else {
            console.error("❌ Função não encontrada:", initFunction);
          }
        };
        document.body.appendChild(script);
      })
      .catch(err => {
        console.error("❌ Erro ao carregar conteúdo AJAX:", err);
      });
  }
}

function fecharConteudo() {
  const conteudo = document.getElementById('conteudo-ajax');
  conteudo.innerHTML = '';
  conteudo.style.display = 'none';
}

function abrirFormularioExercicio(treinoId) {
  console.log("📦 Abrindo formulário para treino:", treinoId);

  fetch(`/usuarios/personal/exercicio-form/${treinoId}/`)
    .then(res => {
      console.log("📤 Resposta do fetch:", res);
      if (!res.ok) {
        throw new Error(`HTTP status ${res.status}`);
      }
      return res.text();
    })
    .then(html => {
      console.log("📥 HTML recebido via fetch:", html);
      const conteudo = document.getElementById('conteudo-ajax');
      if (!conteudo) {
        console.error("❌ Elemento com id 'conteudo-ajax' não encontrado na página!");
        return;
      }
      conteudo.innerHTML = html;
      conteudo.style.display = 'flex';
    })
    .catch(err => {
      alert('Erro ao carregar formulário de exercício');
      console.error("❌ Erro no fetch:", err);
    });
}

