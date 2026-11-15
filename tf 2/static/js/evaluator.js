/* Evaluator page interactions: pick a violation, choose modifiers,
   POST to /api/evaluate, render the verdict panel. */

(function () {
  const list = document.getElementById('vList');
  const modList = document.getElementById('modList');
  const tierWrap = document.getElementById('tierWrap');
  const verdict = document.getElementById('verdict');
  if (!list || !verdict) return;

  let state = {
    slug: null,
    modifiers: new Set(),
    tier: null,
  };

  // Card click -> select
  list.addEventListener('click', (e) => {
    const card = e.target.closest('.violation-card');
    if (!card) return;
    list.querySelectorAll('.violation-card').forEach(c => c.classList.remove('selected'));
    card.classList.add('selected');
    state.slug = card.dataset.slug;
    state.tier = null;
    renderTiers(card.dataset.slug);
    evaluate();
  });

  // Modifier toggle
  modList?.addEventListener('change', (e) => {
    if (e.target.type !== 'checkbox') return;
    const id = e.target.value;
    if (e.target.checked) {
      state.modifiers.add(id);
      e.target.closest('.check-card')?.classList.add('checked');
    } else {
      state.modifiers.delete(id);
      e.target.closest('.check-card')?.classList.remove('checked');
    }
    evaluate();
  });

  function renderTiers(slug) {
    const card = list.querySelector('[data-slug="' + slug + '"]');
    const tiers = JSON.parse(card.dataset.tiers || 'null');
    if (!tiers) {
      tierWrap.innerHTML = '';
      return;
    }
    tierWrap.innerHTML = `
      <div class="eval-step">
        <span class="eval-step-num">Step 2 (optional)</span>
        <h3>How severe?</h3>
        <div class="grid grid-2">
          ${tiers.map((t, i) => `
            <button class="check-card" type="button" data-tier="${i}">
              <div>
                <div class="check-card-text"><strong>${t.label}</strong></div>
                <div style="font-size:.8rem;color:var(--fg-muted);">$${t.fine} · ${t.points} pts</div>
              </div>
            </button>`).join('')}
        </div>
      </div>`;
    tierWrap.querySelectorAll('button').forEach((b) => {
      b.addEventListener('click', () => {
        tierWrap.querySelectorAll('button').forEach(x => x.classList.remove('checked'));
        b.classList.add('checked');
        state.tier = parseInt(b.dataset.tier);
        evaluate();
      });
    });
  }

  async function evaluate() {
    if (!state.slug) return;
    try {
      const res = await fetch('/api/evaluate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          slug: state.slug,
          modifiers: Array.from(state.modifiers),
          tier_index: state.tier,
        }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'failed');
      renderVerdict(data);
    } catch (err) {
      window.toast && window.toast(err.message, 'error');
    }
  }

  function renderVerdict(d) {
    verdict.innerHTML = `
      <div class="eyebrow" style="color:var(--amber-300);">Estimated penalty</div>
      <h2 style="color:#fff;margin:.6rem 0;">${d.violation.name}</h2>
      <div class="verdict-fine">
        $<span data-count="${d.fine_min}" data-duration="900">0</span>
        <small> – $${d.fine_max.toLocaleString()}</small>
      </div>
      <div class="metric-row">
        <div class="metric">
          <div class="metric-label">Points</div>
          <div class="metric-value" data-count="${d.points}" data-duration="800">0</div>
        </div>
        <div class="metric">
          <div class="metric-label">Severity</div>
          <div class="metric-value" style="font-size:1.05rem;text-transform:uppercase;letter-spacing:.08em;">${d.severity_label}</div>
        </div>
        <div class="metric">
          <div class="metric-label">Jail risk</div>
          <div class="metric-value">${d.jail_chance}%</div>
          <div class="risk-bar"><span style="width:0"></span></div>
        </div>
        <div class="metric">
          <div class="metric-label">Suspension risk</div>
          <div class="metric-value">${d.suspend_chance}%</div>
          <div class="risk-bar"><span style="width:0"></span></div>
        </div>
      </div>
      <p style="color:var(--navy-200);font-size:.95rem;margin:0;">${d.summary}</p>
      ${d.modifiers_applied.length ? `
        <div style="margin-top:1rem;display:flex;flex-wrap:wrap;gap:.4rem;">
          ${d.modifiers_applied.map(m => `<span class="pill" style="background:rgba(255,255,255,.1);color:#fde68a;border-color:rgba(245,158,11,.3);">${m.label}</span>`).join('')}
        </div>` : ''}
      <div style="margin-top:1.5rem;display:flex;gap:.5rem;">
        <a class="btn btn-primary btn-sm" href="/violations/${d.violation.slug}">Read full details</a>
      </div>`;

    // Animate counters in verdict
    verdict.querySelectorAll('[data-count]').forEach(el => {
      const target = parseFloat(el.dataset.count);
      const duration = parseInt(el.dataset.duration || '900');
      const start = performance.now();
      function step(now) {
        const t = Math.min(1, (now - start) / duration);
        el.textContent = Math.round(target * (1 - Math.pow(1 - t, 3))).toLocaleString();
        if (t < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    });

    // Animate risk bars
    requestAnimationFrame(() => {
      const bars = verdict.querySelectorAll('.risk-bar > span');
      bars[0].style.width = d.jail_chance + '%';
      bars[1].style.width = d.suspend_chance + '%';
    });

    verdict.classList.remove('shake');
    if (d.severity === 'criminal' || d.severity === 'severe') {
      void verdict.offsetWidth;
      verdict.classList.add('shake');
    }
  }
})();
