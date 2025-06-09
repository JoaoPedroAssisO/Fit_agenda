function iniciarFormularioEdicaoPersonal() {
  const form = document.getElementById('form-editar-personal');
  if (!form) return;

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const formData = new FormData(form);

    fetch('/usuarios/personal/editar_perfil/', {
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
