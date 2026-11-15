/* Stats page - animate horizontal bars when in view */
(function () {
  const bars = document.querySelectorAll('.bar-fill[data-pct]');
  if (!bars.length) return;
  const io = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (en.isIntersecting) {
        en.target.style.width = en.target.dataset.pct + '%';
        io.unobserve(en.target);
      }
    });
  }, { threshold: 0.4 });
  bars.forEach((b) => io.observe(b));
})();
