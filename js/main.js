/* =========================================
   GLENGALA FRESH — main.js
   ========================================= */

const WA_NUMBER = '61434694141';

// ─── Sticky Nav ───────────────────────────
const nav = document.querySelector('.nav');
if (nav) {
  const onScroll = () => {
    nav.classList.toggle('scrolled', window.scrollY > 40);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
}

// ─── Mobile Nav Toggle ────────────────────
const navToggle = document.querySelector('.nav-toggle');
const mobileNav = document.querySelector('.mobile-nav');
if (navToggle && mobileNav) {
  navToggle.addEventListener('click', () => {
    const open = mobileNav.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', String(open));
  });
  // Close on link click
  mobileNav.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => mobileNav.classList.remove('open'));
  });
}

// ─── Scroll Reveal ────────────────────────
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -48px 0px' });

document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

// ─── Accordion ───────────────────────────
document.querySelectorAll('.accordion-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const expanded = btn.getAttribute('aria-expanded') === 'true';
    // Close all others
    document.querySelectorAll('.accordion-btn').forEach(b => b.setAttribute('aria-expanded', 'false'));
    btn.setAttribute('aria-expanded', String(!expanded));
  });
});

// ─── Size Selector ───────────────────────
document.querySelectorAll('.size-selector').forEach(selector => {
  selector.querySelectorAll('.size-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      selector.querySelectorAll('.size-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      // Update displayed price
      const priceDisplay = selector.closest('[data-product]')?.querySelector('.selected-price');
      if (priceDisplay && btn.dataset.price) {
        priceDisplay.textContent = '$' + btn.dataset.price;
      }
    });
  });
  // Activate first by default
  const first = selector.querySelector('.size-btn');
  if (first) first.classList.add('active');
});

// ─── WhatsApp Order Builder ───────────────
function buildWaLink(message) {
  return `https://wa.me/${WA_NUMBER}?text=${encodeURIComponent(message)}`;
}

// Generic product order button
document.querySelectorAll('[data-wa-product]').forEach(btn => {
  btn.addEventListener('click', () => {
    const product = btn.dataset.waProduct;
    const selector = btn.closest('[data-product]')?.querySelector('.size-btn.active');
    const size = selector ? selector.dataset.size : '500ml';
    const price = selector ? '$' + selector.dataset.price : '';
    const msg = `Hi! I'd like to order:\n\n🧃 ${product} — ${size} ${price}\n\nCould you let me know availability and delivery? Thanks!`;
    const url = buildWaLink(msg);
    const newWin = window.open(url, '_blank');
    if (!newWin || newWin.closed || typeof newWin.closed === 'undefined') {
      window.location.href = url;
    }
  });
});

// Contact / order form
const orderForm = document.getElementById('orderForm');
if (orderForm) {
  orderForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const product = orderForm.querySelector('[name="product"]')?.value || '';
    const size    = orderForm.querySelector('[name="size"]')?.value || '';
    const qty     = orderForm.querySelector('[name="qty"]')?.value || '1';
    const name    = orderForm.querySelector('[name="name"]')?.value || '';
    const note    = orderForm.querySelector('[name="note"]')?.value || '';

    const price = getPriceForSize(size);
    const total = price ? `$${(parseFloat(price) * parseInt(qty)).toFixed(2)}` : '';

    let msg = `Hi Glengala Fresh! I'd like to place an order:\n\n`;
    msg += `👤 Name: ${name}\n`;
    msg += `🧃 Product: ${product}\n`;
    msg += `📏 Size: ${size}\n`;
    msg += `🔢 Qty: ${qty}`;
    if (total) msg += `\n💰 Approx total: ${total}`;
    if (note)  msg += `\n📝 Note: ${note}`;
    msg += `\n\nThanks!`;

    window.open(buildWaLink(msg), '_blank');
  });
}

function getPriceForSize(size) {
  const map = { '300ml': '3.99', '500ml': '5.99', '1L': '11.99' };
  return map[size] || '';
}

// Partnership interest form
const partnerForm = document.getElementById('partnerForm');
if (partnerForm) {
  partnerForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const name    = partnerForm.querySelector('[name="name"]')?.value || '';
    const gym     = partnerForm.querySelector('[name="gym"]')?.value || '';
    const tier    = partnerForm.querySelector('[name="tier"]')?.value || '';
    const message = partnerForm.querySelector('[name="message"]')?.value || '';

    let msg = `Hi! I'm interested in a Glengala Fresh partnership.\n\n`;
    msg += `👤 Name: ${name}\n`;
    msg += `🏋️ Business: ${gym}\n`;
    msg += `📦 Tier: ${tier}`;
    if (message) msg += `\n💬 Message: ${message}`;

    window.open(buildWaLink(msg), '_blank');
  });
}

// ─── Blog Category Filter ─────────────────
const filterBtns = document.querySelectorAll('[data-filter]');
const articleCards = document.querySelectorAll('[data-category]');
if (filterBtns.length && articleCards.length) {
  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const filter = btn.dataset.filter;
      articleCards.forEach(card => {
        const match = filter === 'all' || card.dataset.category === filter;
        card.style.display = match ? '' : 'none';
      });
    });
  });
}

// ─── Smooth scroll for anchor links ──────
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

// ─── Service Worker ───────────────────────
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js').catch(() => {});
  });
}
