function carregarSecao(secao) {
  let url = '';

  if (secao === 'editar_personal') {
    url = '/usuarios/personal/editar_perfil/';
  } else if (secao === 'editar_dados') {
  url = '/usuarios/personal/editar-dados-form/';
}

  if (url) {
    fetch(url)
      .then(response => response.text())
      .then(html => {
        const conteudo = document.getElementById('conteudo-ajax');
        conteudo.innerHTML = html;
        conteudo.style.display = 'flex';

        const script = document.createElement("script");
        script.src = "/static/usuarios/js/editar_perfil_personal_ajax.js";
        script.onload = () => {
          iniciarFormularioEdicaoPersonal();
        };
        document.body.appendChild(script);
      });
  }
}

function fecharConteudo() {
  const conteudo = document.getElementById('conteudo-ajax');
  conteudo.innerHTML = '';
  conteudo.style.display = 'none';
}
