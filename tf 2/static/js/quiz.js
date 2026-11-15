/* Knowledge Quiz - 1 question per screen, scoring, confetti at end */
(function () {
  const shell = document.getElementById('quizShell');
  if (!shell) return;
  let questions = [];
  let i = 0;
  let score = 0;
  let answered = false;

  async function start() {
    const res = await fetch('/api/quiz');
    questions = await res.json();
    i = 0; score = 0;
    render();
  }

  function render() {
    answered = false;
    if (i >= questions.length) {
      renderDone();
      return;
    }
    const q = questions[i];
    shell.innerHTML = `
      <div class="quiz-progress">
        <span>Question ${i + 1} / ${questions.length}</span>
        <span>Score ${score}</span>
      </div>
      <div class="progress" style="margin-bottom:1.25rem;"><div class="progress-fill" style="width:${(i / questions.length) * 100}%"></div></div>
      <div class="quiz-card reveal in">
        <div class="eyebrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>Quiz</div>
        <h3 class="quiz-question">${q.question}</h3>
        <div class="quiz-options">
          ${q.options.map((o, idx) => `<button class="quiz-option" data-idx="${idx}">${String.fromCharCode(65 + idx)}. ${o}</button>`).join('')}
        </div>
        <div id="quizAfter"></div>
      </div>`;

    shell.querySelectorAll('.quiz-option').forEach((b) => {
      b.addEventListener('click', () => answer(parseInt(b.dataset.idx), q));
    });
  }

  function answer(idx, q) {
    if (answered) return;
    answered = true;
    const buttons = shell.querySelectorAll('.quiz-option');
    buttons.forEach((b, bi) => {
      b.classList.add('disabled');
      if (bi === q.answer) b.classList.add('correct');
      else if (bi === idx) b.classList.add('wrong');
    });
    if (idx === q.answer) score++;

    document.getElementById('quizAfter').innerHTML = `
      <div class="quiz-explain"><strong>${idx === q.answer ? 'Correct.' : 'Not quite.'}</strong> ${q.explain}</div>
      <div style="margin-top:1rem;text-align:right;">
        <button class="btn btn-primary" id="quizNext">${i + 1 === questions.length ? 'See results' : 'Next question'} →</button>
      </div>`;
    document.getElementById('quizNext').addEventListener('click', () => {
      i++;
      render();
    });
  }

  function renderDone() {
    const pct = Math.round((score / questions.length) * 100);
    let label = 'Try again';
    if (pct >= 90) label = 'Defensive driving champion.';
    else if (pct >= 70) label = 'You know the rules well.';
    else if (pct >= 50) label = 'Solid foundation - room to grow.';
    else label = 'Time to brush up on the basics.';

    shell.innerHTML = `
      <div class="quiz-result">
        <div class="eyebrow" style="justify-content:center;">Results</div>
        <div class="quiz-score">${score}/${questions.length}</div>
        <p style="font-size:1.1rem;margin:.5rem 0;">${label}</p>
        <p style="color:var(--fg-muted);">You scored ${pct}%.</p>
        <div style="margin-top:1.5rem;display:flex;gap:.5rem;justify-content:center;">
          <button class="btn btn-primary" id="quizAgain">Play again</button>
          <a class="btn btn-outline" href="/violations">Browse violations</a>
        </div>
      </div>`;
    document.getElementById('quizAgain').addEventListener('click', start);
    if (pct >= 50) confetti();
  }

  function confetti() {
    const host = document.createElement('div');
    host.className = 'confetti-host';
    document.body.appendChild(host);
    const colors = ['#f59e0b', '#d97706', '#10b981', '#3b82f6', '#ef4444', '#fbbf24'];
    for (let i = 0; i < 90; i++) {
      const p = document.createElement('div');
      p.className = 'confetti-piece';
      p.style.left = Math.random() * 100 + '%';
      p.style.background = colors[i % colors.length];
      p.style.setProperty('--dx', (Math.random() * 200 - 100) + 'px');
      p.style.animationDelay = (Math.random() * 0.4) + 's';
      host.appendChild(p);
    }
    setTimeout(() => host.remove(), 3500);
  }

  start();
})();
