/* Violations catalogue: search + severity filter + category filter */
(function () {
  const grid = document.getElementById('vGrid');
  if (!grid) return;
  const search = document.getElementById('vSearch');
  const severityChips = document.querySelectorAll('[data-sev]');
  const catChips = document.querySelectorAll('[data-cat]');

  let activeSev = 'all';
  let activeCat = 'all';

  function apply() {
    const q = (search?.value || '').trim().toLowerCase();
    let shown = 0;
    grid.querySelectorAll('.v-tile').forEach((tile) => {
      const matchSev = activeSev === 'all' || tile.dataset.sev === activeSev;
      const matchCat = activeCat === 'all' || tile.dataset.cat === activeCat;
      const text = tile.textContent.toLowerCase();
      const matchQ = !q || text.includes(q);
      const ok = matchSev && matchCat && matchQ;
      tile.style.display = ok ? '' : 'none';
      if (ok) shown++;
    });
    const empty = document.getElementById('vEmpty');
    if (empty) empty.style.display = shown === 0 ? '' : 'none';
  }

  search?.addEventListener('input', apply);

  severityChips.forEach((c) => {
    c.addEventListener('click', () => {
      severityChips.forEach((x) => x.classList.remove('active'));
      c.classList.add('active');
      activeSev = c.dataset.sev;
      apply();
    });
  });
  catChips.forEach((c) => {
    c.addEventListener('click', () => {
      catChips.forEach((x) => x.classList.remove('active'));
      c.classList.add('active');
      activeCat = c.dataset.cat;
      apply();
    });
  });
})();
