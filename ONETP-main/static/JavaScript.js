

  function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const modoOscuroActivo = document.body.classList.contains('dark-mode');
    localStorage.setItem('modoOscuro', modoOscuroActivo);
  }

  window.onload = function () {
    const modoOscuroGuardado = localStorage.getItem('modoOscuro') === 'true';
    if (modoOscuroGuardado) {
      document.body.classList.add('dark-mode');
    }

    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('toggleBtn');

    if (toggleBtn && sidebar) {
      toggleBtn.addEventListener('click', () => {
        sidebar.classList.toggle('collapsed');
        sidebar.classList.toggle('expanded');
      });
    }
  };




  
