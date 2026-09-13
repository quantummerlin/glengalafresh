/* =========================================
   GLENGALA FRESH — main.js
   ========================================= */

const PHONE_NUMBER = '61434694141';

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
  // Close on link click — delay so iOS doesn't cancel navigation before href fires
  mobileNav.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => setTimeout(() => mobileNav.classList.remove('open'), 100));
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
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      e.preventDefault();
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

// ─── Campaign Source Tracking ─────────────
// Reads utm_* / ref params from the URL so every order message and Plausible
// event can be attributed back to the social post, QR code or partner link.
function getCampaignSource() {
  try {
    var params = new URLSearchParams(window.location.search);
    var source = params.get('utm_source') || params.get('src') || '';
    var medium = params.get('utm_medium') || params.get('utm_campaign') || params.get('bundle') || '';
    var bits = [source, medium].filter(Boolean);
    return bits.length ? bits.join('/') : '';
  } catch (e) {
    return '';
  }
}

function withSource(msg) {
  var src = getCampaignSource();
  return src ? msg + '\n\n(seen via: ' + src + ')' : msg;
}

// ─── Analytics Events ─────────────────────
function trackEvent(name, props) {
  try {
    if (typeof window.plausible === 'function') window.plausible(name, { props: props || {} });
  } catch (e) {}
}

// ─── SMS Order Builder ───────────────────
function buildSmsLink(message) {
  const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
  const sep = isIOS ? '&' : '?';
  return `sms:+${PHONE_NUMBER}${sep}body=${encodeURIComponent(message)}`;
}

// Convert any leftover wa.me links on the page to SMS at runtime
document.querySelectorAll('a[href*="wa.me"]').forEach(a => {
  const url = new URL(a.href);
  const text = url.searchParams.get('text') || '';
  a.href = buildSmsLink(text);
  a.removeAttribute('target');
  a.addEventListener('click', () => trackEvent('Whatsapp Open', { source: getCampaignSource() || 'direct-link' }));
});

// Generic product order button
document.querySelectorAll('[data-wa-product]').forEach(btn => {
  btn.addEventListener('click', () => {
    const product = btn.dataset.waProduct;
    const selector = btn.closest('[data-product]')?.querySelector('.size-btn.active');
    const size = selector ? selector.dataset.size : '500ml';
    const price = selector ? '$' + selector.dataset.price : '';
    let msg = `Hi! I'd like to order:\n\n${product} — ${size} ${price}\n\nCould you let me know availability and delivery? Thanks!`;
    msg = withSource(msg);
    trackEvent('Order Intent', { product: product, size: size, source: getCampaignSource() || 'organic' });
    window.location.href = buildSmsLink(msg);
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
    const fulfil  = orderForm.querySelector('[name="fulfilment"]')?.value || '';
    const suburb  = orderForm.querySelector('[name="suburb"]')?.value || '';

    const price = getPriceForSize(size);
    const total = price ? `$${(parseFloat(price) * parseInt(qty)).toFixed(2)}` : '';

    let msg = `Hi Glengala Fresh! I'd like to place an order:\n\n`;
    msg += `👤 Name: ${name}\n`;
    msg += `🧃 Product: ${product}\n`;
    msg += `📏 Size: ${size}\n`;
    msg += `🔢 Qty: ${qty}`;
    if (fulfil) msg += `\n🚚 ${fulfil}`;
    if (suburb) msg += `\n📍 Suburb: ${suburb}`;
    if (total) msg += `\n💰 Approx total: ${total}`;
    if (note)  msg += `\n📝 Note: ${note}`;
    msg += `\n\nThanks!`;
    msg = withSource(msg);

    trackEvent('Order Submitted', { product: product, size: size, qty: qty, fulfilment: fulfil, source: getCampaignSource() || 'organic' });
    window.location.href = buildSmsLink(msg);
  });
}

function getPriceForSize(size) {
  const map = { '300ml': '3.99', '500ml': '5.99', '1L': '11.99' };
  return map[size] || '';
}

// Lemonade has a different price tier
function getLemonadePriceForSize(size) {
  const map = { '300ml': '1.99', '500ml': '2.99', '1L': '5.99' };
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
    msg = withSource(msg);

    trackEvent('Partner Enquiry', { tier: tier, source: getCampaignSource() || 'organic' });
    window.location.href = buildSmsLink(msg);
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

// ─── Site-wide Disclaimer ─────────────────
// Injected once, below every page footer, so compliance language is consistent
// across shop, product, article and partnership pages.
(function injectDisclaimer() {
  var footer = document.querySelector('footer.footer');
  if (!footer || document.getElementById('gf-disclaimer')) return;
  var box = document.createElement('div');
  box.id = 'gf-disclaimer';
  box.style.cssText = 'border-top:1px solid rgba(255,255,255,0.08);padding:24px 0;margin-top:24px;';
  box.innerHTML =
    '<div class="container" style="max-width:900px;">' +
    '<p style="font-size:0.75rem;line-height:1.7;color:rgba(255,255,255,0.45);margin:0;">' +
    '<strong>Important:</strong> Glengala Fresh juices are fresh, unpasteurised food products. They are not medicines and are not intended to diagnose, treat, cure or prevent any disease. Keep refrigerated at 5°C or below and consume within 3–5 days. Unpasteurised juice is not recommended for pregnant women, young children, older adults, or people with weakened immune systems. If you take medication or are managing a health condition, check with your doctor or dietitian before adding these juices to your routine. Information on this site is general in nature. All prices in AUD, including GST.</p>' +
    '</div>';
  footer.appendChild(box);
})();
