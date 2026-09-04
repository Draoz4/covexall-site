/* ===========================================================
   Covexall — home page behaviour
   Edit LINKS below to point buttons at the live store / pages.
   =========================================================== */
const LINKS = {
  shop: 'https://covexall.com',
  wholesale: 'https://covexall.com',
  contact: 'https://covexall.com',
  privacy: '#',
  terms: '#',
  facebook: '#',
  instagram: '#',
  tiktok: '#',
  youtube: '#',
};
const CHAT_WEBHOOK = 'https://n8n.nutricove.co/webhook/covexall-rag';

/* ---------- link wiring ---------- */
document.querySelectorAll('[data-link]').forEach((a) => {
  const target = LINKS[a.dataset.link];
  if (!target || target === '#') return;
  a.href = target;
  if (/^https?:/.test(target)) { a.target = '_blank'; a.rel = 'noopener'; }
});

/* ---------- nav ---------- */
const navWrap = document.querySelector('.nav-wrap');
const toggle = document.querySelector('.nav-toggle');
const links = document.getElementById('nav-links');
const onScroll = () => navWrap.classList.toggle('scrolled', window.scrollY > 24);
onScroll();
window.addEventListener('scroll', onScroll, { passive: true });
toggle.addEventListener('click', () => {
  const open = links.classList.toggle('open');
  toggle.setAttribute('aria-expanded', String(open));
  toggle.classList.toggle('active', open);
  document.body.classList.toggle('menu-open', open);
});
links.querySelectorAll('a').forEach((a) => a.addEventListener('click', () => {
  links.classList.remove('open'); toggle.classList.remove('active');
  toggle.setAttribute('aria-expanded', 'false'); document.body.classList.remove('menu-open');
}));

/* active section highlight */
const sections = [...document.querySelectorAll('main section[id]')];
const navAnchors = [...links.querySelectorAll('a[href^="#"]')];
const spy = new IntersectionObserver((entries) => {
  entries.forEach((e) => {
    if (!e.isIntersecting) return;
    navAnchors.forEach((a) => a.classList.toggle('active', a.getAttribute('href') === '#' + e.target.id));
  });
}, { rootMargin: '-40% 0px -55% 0px' });
sections.forEach((s) => spy.observe(s));

/* ---------- reveal on scroll ---------- */
const reveals = document.querySelectorAll('.reveal');
if (location.search.includes('noanim')) {
  reveals.forEach((el) => el.classList.add('in'));
} else if ('IntersectionObserver' in window) {
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
  reveals.forEach((el, i) => { el.style.setProperty('--d', `${(i % 4) * 70}ms`); io.observe(el); });
} else {
  reveals.forEach((el) => el.classList.add('in'));
}

/* ---------- hero parallax (subtle) ---------- */
const hero = document.querySelector('.hero-visual');
if (hero && matchMedia('(pointer:fine)').matches) {
  const layers = hero.querySelectorAll('.hv-bac, .hv-viro, .hv-snot, .hv-cove');
  hero.parentElement.addEventListener('mousemove', (ev) => {
    const r = hero.getBoundingClientRect();
    const dx = (ev.clientX - (r.left + r.width / 2)) / r.width;
    const dy = (ev.clientY - (r.top + r.height / 2)) / r.height;
    layers.forEach((l, i) => {
      const k = [10, 16, 22, 6][i];
      l.style.setProperty('--px', `${dx * k}px`);
      l.style.setProperty('--py', `${dy * k}px`);
    });
  });
}

/* ---------- FAQ: only one open at a time ---------- */
const faqs = document.querySelectorAll('.faq-list details');
faqs.forEach((d) => d.addEventListener('toggle', () => {
  if (d.open) faqs.forEach((o) => { if (o !== d) o.open = false; });
}));

/* ---------- newsletter (front-end only) ---------- */
document.querySelectorAll('[data-form="newsletter"]').forEach((form) => {
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const email = form.querySelector('input[type="email"]').value.trim();
    const status = form.querySelector('.nl-status');
    if (!email) return;
    try {
      const list = JSON.parse(localStorage.getItem('cvx_subscribers') || '[]');
      if (!list.includes(email)) list.push(email);
      localStorage.setItem('cvx_subscribers', JSON.stringify(list));
    } catch (_) { /* storage unavailable */ }
    status.textContent = "You're in! Cove will keep you posted.";
    form.reset();
  });
});

/* ---------- footer year ---------- */
document.querySelectorAll('[data-year]').forEach((el) => { el.textContent = new Date().getFullYear(); });

/* ---------- Ask Cove chat ---------- */
(() => {
  const btn = document.getElementById('cx-toggle');
  const win = document.getElementById('cx-window');
  const close = document.getElementById('cx-close');
  const list = document.getElementById('cx-messages');
  const form = document.getElementById('cx-form');
  const input = document.getElementById('cx-input');
  const send = document.getElementById('cx-send');
  if (!btn || !win) return;

  let chatId = null;
  try {
    chatId = sessionStorage.getItem('cx_session_id');
    if (!chatId) { chatId = 'cx-' + Date.now() + '-' + Math.random().toString(36).slice(2, 8); sessionStorage.setItem('cx_session_id', chatId); }
  } catch (_) { chatId = 'cx-' + Date.now(); }

  const esc = (t) => t.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const fmt = (t) => esc(t).replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>');
  const add = (type, text) => {
    const el = document.createElement('div');
    el.className = 'cx-msg ' + type;
    if (type === 'typing') el.innerHTML = '<span></span><span></span><span></span>';
    else el.innerHTML = fmt(text);
    list.appendChild(el); list.scrollTop = list.scrollHeight; return el;
  };

  let greeted = false; let sending = false;
  const open = () => {
    win.hidden = false; btn.setAttribute('aria-expanded', 'true'); btn.classList.add('open');
    requestAnimationFrame(() => win.classList.add('visible'));
    if (!greeted) { greeted = true; add('bot', "Hey! 👋 I'm Cove. Ask me anything about Covexall — how long it protects, what it's tested against, sizes, or which bottle is right for you."); }
    setTimeout(() => input.focus(), 250);
  };
  const shut = () => {
    win.classList.remove('visible'); btn.setAttribute('aria-expanded', 'false'); btn.classList.remove('open');
    setTimeout(() => { win.hidden = true; }, 220);
  };
  btn.addEventListener('click', () => (win.hidden ? open() : shut()));
  close.addEventListener('click', shut);
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !win.hidden) shut(); });

  const ask = async () => {
    const text = input.value.trim();
    if (!text || sending) return;
    add('user', text); input.value = ''; input.style.height = '';
    sending = true; send.disabled = true;
    const typing = add('typing');
    try {
      const res = await fetch(CHAT_WEBHOOK, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ message: text, chatId }) });
      const data = await res.json();
      const reply = data.output || data.text || data.response || data.message || "Sorry, I didn't catch that. Try again?";
      typing.remove(); add('bot', reply);
    } catch (_) {
      typing.remove(); add('bot', 'Something went wrong on my end. Please try again in a moment.');
    }
    sending = false; send.disabled = false; input.focus();
  };
  form.addEventListener('submit', (e) => { e.preventDefault(); ask(); });
  input.addEventListener('keydown', (e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); ask(); } });
  input.addEventListener('input', () => { input.style.height = 'auto'; input.style.height = Math.min(input.scrollHeight, 120) + 'px'; });
})();
