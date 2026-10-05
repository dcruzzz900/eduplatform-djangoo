/**
 * PWA registration + install prompt
 */
(function () {
  if (!('serviceWorker' in navigator)) return;

  window.addEventListener('load', function () {
    navigator.serviceWorker
      .register('/sw.js', { scope: '/' })
      .then(function (reg) {
        console.log('[PWA] SW registered', reg.scope);
      })
      .catch(function (err) {
        console.warn('[PWA] SW registration failed', err);
      });
  });

  var deferredPrompt = null;
  var installBtn = document.getElementById('pwa-install-btn');

  window.addEventListener('beforeinstallprompt', function (e) {
    e.preventDefault();
    deferredPrompt = e;
    if (installBtn) {
      installBtn.hidden = false;
    }
  });

  if (installBtn) {
    installBtn.addEventListener('click', function () {
      if (!deferredPrompt) return;
      deferredPrompt.prompt();
      deferredPrompt.userChoice.then(function () {
        deferredPrompt = null;
        installBtn.hidden = true;
      });
    });
  }

  window.addEventListener('appinstalled', function () {
    if (installBtn) installBtn.hidden = true;
    deferredPrompt = null;
  });

  // Online/offline banner
  function setOnlineState() {
    var el = document.getElementById('offline-banner');
    if (!el) return;
    el.hidden = navigator.onLine;
  }
  window.addEventListener('online', setOnlineState);
  window.addEventListener('offline', setOnlineState);
  setOnlineState();
})();
