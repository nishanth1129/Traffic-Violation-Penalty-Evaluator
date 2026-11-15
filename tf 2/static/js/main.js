/* ============================================================
   PenaltyEval - Core JS
   - Theme toggle
   - Mobile nav
   - Reveal-on-scroll
   - Animated counters
   - Particle field
   - Toast helper
   ============================================================ */

(function () {
  'use strict';

  // -------- Theme --------
  const THEME_KEY = 'penalty-eval-theme';
  const root = document.documentElement;

  function applyTheme(t) {
    root.setAttribute('data-theme', t);
    const btn = document.querySelector('.theme-toggle svg use');
    const sun = document.querySelector('.theme-toggle .icon-sun');
    const moon = document.querySelector('.theme-toggle .icon-moon');
    if (sun && moon) {
      sun.style.display = t === 'dark' ? 'block' : 'none';
      moon.style.display = t === 'dark' ? 'none' : 'block';
    }
  }
  const saved = localStorage.getItem(THEME_KEY) || 'light';
  applyTheme(saved);

  document.addEventListener('click', (e) => {
    const t = e.target.closest('.theme-toggle');
    if (!t) return;
    const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    localStorage.setItem(THEME_KEY, next);
    applyTheme(next);
  });

  // -------- Mobile nav --------
  document.addEventListener('click', (e) => {
    if (e.target.closest('.menu-toggle')) {
      document.querySelector('.nav-links')?.classList.toggle('open');
    }
  });

  // -------- Reveal on scroll --------
  const io = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (en.isIntersecting) {
        en.target.classList.add('in');
        io.unobserve(en.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
  document.querySelectorAll('.reveal, .reveal-stagger').forEach((el) => io.observe(el));

  // -------- Animated counters --------
  function animateCounter(el) {
    const target = parseFloat(el.dataset.count || el.textContent.replace(/[^0-9.]/g, ''));
    const decimals = (el.dataset.decimals && parseInt(el.dataset.decimals)) || 0;
    const duration = parseInt(el.dataset.duration || '1400');
    const prefix = el.dataset.prefix || '';
    const suffix = el.dataset.suffix || '';
    const start = performance.now();
    const fmt = (n) => prefix + n.toLocaleString(undefined,
      { maximumFractionDigits: decimals, minimumFractionDigits: decimals }) + suffix;

    function step(now) {
      const t = Math.min(1, (now - start) / duration);
      const eased = 1 - Math.pow(1 - t, 3);
      el.textContent = fmt(target * eased);
      if (t < 1) requestAnimationFrame(step);
      else el.textContent = fmt(target);
    }
    requestAnimationFrame(step);
  }

  const counterIO = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (en.isIntersecting) {
        animateCounter(en.target);
        counterIO.unobserve(en.target);
      }
    });
  }, { threshold: 0.4 });
  document.querySelectorAll('[data-count]').forEach((el) => counterIO.observe(el));

  // -------- Particle field --------
  const particleHosts = document.querySelectorAll('[data-particles]');
  particleHosts.forEach((host) => {
    const n = parseInt(host.dataset.particles) || 18;
    for (let i = 0; i < n; i++) {
      const s = document.createElement('span');
      const size = 4 + Math.random() * 12;
      s.style.width = size + 'px';
      s.style.height = size + 'px';
      s.style.left = Math.random() * 100 + '%';
      s.style.bottom = -20 + Math.random() * 40 + 'px';
      s.style.animationDelay = (Math.random() * 18) + 's';
      s.style.animationDuration = (12 + Math.random() * 16) + 's';
      host.appendChild(s);
    }
  });

  // -------- Toast --------
  let host;
  function ensureHost() {
    if (!host) {
      host = document.createElement('div');
      host.className = 'toast-host';
      document.body.appendChild(host);
    }
    return host;
  }
  window.toast = function (msg, type = 'info', timeout = 3500) {
    const t = document.createElement('div');
    t.className = 'toast' + (type ? ' ' + type : '');
    t.textContent = msg;
    ensureHost().appendChild(t);
    setTimeout(() => {
      t.style.opacity = '0';
      t.style.transform = 'translateX(120%)';
      t.style.transition = 'all 0.4s';
      setTimeout(() => t.remove(), 450);
    }, timeout);
  };

  // -------- Traffic light cycle (decorative) --------
  function cycleLight(host) {
    const dots = host.querySelectorAll('.tl-dot');
    const seq = ['red', 'red', 'green', 'green', 'yellow'];
    let i = 0;
    setInterval(() => {
      dots.forEach((d) => d.classList.remove('on'));
      const cls = seq[i % seq.length];
      host.querySelector('.tl-dot.' + cls)?.classList.add('on');
      i++;
    }, 1300);
  }
  document.querySelectorAll('.traffic-light').forEach(cycleLight);

  // -------- Tilt effect --------
  document.querySelectorAll('[data-tilt]').forEach((el) => {
    el.addEventListener('mousemove', (e) => {
      const r = el.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width - 0.5;
      const y = (e.clientY - r.top) / r.height - 0.5;
      el.style.transform = `perspective(700px) rotateY(${x * 8}deg) rotateX(${-y * 8}deg) translateY(-3px)`;
    });
    el.addEventListener('mouseleave', () => { el.style.transform = ''; });
  });
})();
