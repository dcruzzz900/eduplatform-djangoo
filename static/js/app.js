/**
 * EduPlatform — responsive UI helpers
 * Mobile / tablet nav, flashes, offline, attendance queue
 */
(function () {
  var toggle = document.getElementById('menu-toggle');
  var sidebar = document.getElementById('sidebar');
  var backdrop = document.getElementById('sidebar-backdrop');

  function openMenu() {
    if (!sidebar) return;
    sidebar.classList.add('open');
    document.body.classList.add('nav-open');
    if (toggle) toggle.setAttribute('aria-expanded', 'true');
    if (backdrop) {
      backdrop.hidden = false;
      requestAnimationFrame(function () {
        backdrop.classList.add('visible');
      });
    }
  }

  function closeMenu() {
    if (!sidebar) return;
    sidebar.classList.remove('open');
    document.body.classList.remove('nav-open');
    if (toggle) toggle.setAttribute('aria-expanded', 'false');
    if (backdrop) {
      backdrop.classList.remove('visible');
      setTimeout(function () {
        backdrop.hidden = true;
      }, 220);
    }
  }

  function isMobileNav() {
    return window.matchMedia('(max-width: 1024px)').matches;
  }

  if (toggle) {
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-controls', 'sidebar');
    toggle.addEventListener('click', function () {
      if (sidebar && sidebar.classList.contains('open')) closeMenu();
      else openMenu();
    });
  }

  if (backdrop) backdrop.addEventListener('click', closeMenu);

  document.querySelectorAll('.nav-link').forEach(function (link) {
    link.addEventListener('click', function () {
      if (isMobileNav()) closeMenu();
    });
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeMenu();
  });

  window.addEventListener('resize', function () {
    if (!isMobileNav()) closeMenu();
  });

  // Confirm destructive actions
  document.querySelectorAll('[data-confirm]').forEach(function (el) {
    el.addEventListener('click', function (e) {
      if (!confirm(el.getAttribute('data-confirm') || 'Are you sure?')) {
        e.preventDefault();
      }
    });
  });

  // Auto-hide flash messages
  setTimeout(function () {
    document.querySelectorAll('.flash').forEach(function (f) {
      f.style.transition = 'opacity .4s';
      f.style.opacity = '0';
    });
  }, 5000);

  // Online / offline banner
  function updateOnline() {
    var banner = document.getElementById('offline-banner');
    if (!banner) return;
    banner.hidden = navigator.onLine;
  }
  window.addEventListener('online', updateOnline);
  window.addEventListener('offline', updateOnline);
  updateOnline();

  // Attendance offline queue sync hint
  window.addEventListener('online', function () {
    try {
      var q = JSON.parse(localStorage.getItem('eduplatform_attendance_queue') || '[]');
      if (q.length && 'serviceWorker' in navigator && navigator.serviceWorker.controller) {
        navigator.serviceWorker.ready.then(function (reg) {
          if (reg.sync) reg.sync.register('attendance-sync').catch(function () {});
        });
      }
    } catch (e) {}
  });
})();
