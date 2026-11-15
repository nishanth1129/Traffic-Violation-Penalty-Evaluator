/* Points simulator - slider with live status update + animated arc */
(function () {
  const slider = document.getElementById('pSlider');
  const display = document.getElementById('pDisplay');
  const meterArc = document.getElementById('pArc');
  const statusBox = document.getElementById('pStatus');
  const ladder = document.querySelectorAll('[data-threshold]');
  if (!slider) return;

  async function update() {
    const v = parseInt(slider.value);
    display.textContent = v;
    slider.style.setProperty('--val', (v / parseInt(slider.max)) * 100 + '%');

    const res = await fetch('/api/points/' + v);
    const d = await res.json();
    statusBox.querySelector('.pstatus-label').textContent = d.label;
    statusBox.querySelector('.pstatus-msg').textContent = d.message;
    statusBox.dataset.tone = d.tone;

    // Arc fill
    const pct = Math.min(1, v / 20);
    if (meterArc) {
      const len = 220 * Math.PI;
      meterArc.style.strokeDasharray = `${len * pct} ${len}`;
    }

    // Highlight active ladder row
    ladder.forEach((row) => row.classList.remove('active'));
    let chosen = ladder[ladder.length - 1];
    for (const row of ladder) {
      if (v <= parseInt(row.dataset.threshold)) {
        chosen = row;
        break;
      }
    }
    chosen?.classList.add('active');
  }

  slider.addEventListener('input', update);
  update();
})();
