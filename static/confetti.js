// static/confetti.js
// Minimal fallback confetti (no external libs)
window.launchConfetti = function () {
  const body = document.body;
  for (let i = 0; i < 60; i++) {
    const s = document.createElement('span');
    s.textContent = "🎉";
    s.style.position = 'fixed';
    s.style.left = Math.random() * 100 + 'vw';
    s.style.top = '-2rem';
    s.style.fontSize = (Math.random() * 12 + 14) + 'px';
    s.style.transition = 'transform 1.2s ease, opacity 1.2s ease';
    s.style.zIndex = 9999;
    body.appendChild(s);
    requestAnimationFrame(() => {
      s.style.transform = `translateY(${100 + Math.random() * 80}vh) rotate(${Math.random()*360}deg)`;
      s.style.opacity = 0;
    });
    setTimeout(() => s.remove(), 1300);
  }
};
