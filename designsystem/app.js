const polarityCard = document.querySelector('.polarity-card');
const polarityButtons = [...document.querySelectorAll('[data-polarity]')];
const signValue = document.querySelector('.sign-value');
const polarityStatus = document.querySelector('.polarity-status');
const toast = document.querySelector('.toast');

let toastTimer;
function announce(message) {
  toast.textContent = message;
  toast.classList.add('show');
  window.clearTimeout(toastTimer);
  toastTimer = window.setTimeout(() => toast.classList.remove('show'), 1800);
}

function setPolarity(next) {
  const isPositive = next === 'positive';
  polarityCard.dataset.state = next;
  signValue.textContent = isPositive ? '+' : '−';
  polarityStatus.textContent = isPositive ? 'Positiv' : 'Negativ';
  polarityButtons.forEach((button) => {
    const active = button.dataset.polarity === next;
    button.classList.toggle('active', active);
    button.setAttribute('aria-pressed', String(active));
  });
  announce(`Ausgang auf ${isPositive ? 'positive' : 'negative'} Polarität geschaltet`);
}

polarityButtons.forEach((button) => {
  button.addEventListener('click', () => setPolarity(button.dataset.polarity));
});

const toggleCard = document.querySelector('.toggle-card');
const guardButton = document.querySelector('.safety-guard');
const toggleButton = document.querySelector('.toggle-lever');
const toggleStatus = document.querySelector('.toggle-status');
const footerToggleStatus = document.querySelector('.footer-toggle-status');

function setGuard(open) {
  toggleCard.classList.toggle('guard-open', open);
  guardButton.setAttribute('aria-expanded', String(open));
  guardButton.setAttribute('aria-label', open ? 'Schutzklappe schließen' : 'Schutzklappe öffnen');
  if (open) {
    window.setTimeout(() => toggleButton.focus({ preventScroll: true }), 320);
  }
}

function setToggle(on) {
  toggleCard.dataset.state = on ? 'on' : 'off';
  toggleButton.setAttribute('aria-checked', String(on));
  toggleStatus.textContent = on ? 'Aktiv' : 'Standby';
  footerToggleStatus.textContent = on ? 'Aktiv' : 'Standby';
  announce(`Klappschalter ${on ? 'aktiviert' : 'auf Standby gesetzt'}`);
  if (!on) window.setTimeout(() => setGuard(false), 240);
}

guardButton.addEventListener('click', () => {
  const isOpen = guardButton.getAttribute('aria-expanded') === 'true';
  const isOn = toggleButton.getAttribute('aria-checked') === 'true';
  if (isOn && isOpen) {
    setToggle(false);
  } else {
    setGuard(!isOpen);
    announce(isOpen ? 'Schutzklappe geschlossen' : 'Schutzklappe geöffnet');
  }
});

toggleButton.addEventListener('click', () => {
  if (!toggleCard.classList.contains('guard-open')) return;
  const isOn = toggleButton.getAttribute('aria-checked') === 'true';
  setToggle(!isOn);
});

toggleButton.addEventListener('keydown', (event) => {
  if (event.key === 'Enter' || event.key === ' ') {
    event.preventDefault();
    toggleButton.click();
  }
});

// Subtle, bounded parallax for the hero mark on fine pointers only.
const heroVisual = document.querySelector('.hero-visual');
const heroMonogram = document.querySelector('.hero-monogram');
if (window.matchMedia('(pointer:fine) and (prefers-reduced-motion:no-preference)').matches) {
  heroVisual.addEventListener('pointermove', (event) => {
    const rect = heroVisual.getBoundingClientRect();
    const x = (event.clientX - rect.left) / rect.width - 0.5;
    const y = (event.clientY - rect.top) / rect.height - 0.5;
    heroMonogram.style.transform = `translate(calc(-50% + ${x * 12}px), calc(-50% + ${y * 12}px))`;
  });
  heroVisual.addEventListener('pointerleave', () => {
    heroMonogram.style.transform = 'translate(-50%, -50%)';
  });
}
