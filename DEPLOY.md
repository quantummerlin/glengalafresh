# Glengala Fresh — Deployment Guide

## How This Site Works

**Static site.** No backend, no database, no build step. Just HTML, CSS, and JS files.

**Hosting:** GitHub Pages (free)
**Domain:** glengalafresh.au
**Analytics:** Plausible (privacy-friendly)
**Orders:** SMS via `sms:` links (opens native messaging app)

## Deployment Workflow

### Making Changes

1. Edit files locally in `/c/Users/WIPED/glengalafreshjuice/`
2. Test locally by opening `index.html` in a browser
3. Commit and push to `main`:
   ```bash
   cd /c/Users/WIPED/glengalafreshjuice
   git add -A
   git commit -m "Description of changes"
   git push origin main
   ```
4. GitHub Actions auto-deploys to GitHub Pages (takes ~1-2 minutes)
5. Verify at https://glengalafresh.au

### Safer Workflow (for bigger changes)

1. Create a new branch:
   ```bash
   git checkout -b feature/my-change
   ```
2. Make changes, commit, push:
   ```bash
   git push origin feature/my-change
   ```
3. Open a Pull Request on GitHub
4. The PR check runs automatically (validates links, SEO, analytics)
5. Review the PR, then merge to `main`
6. Auto-deploy kicks in

## File Structure

```
glengalafreshjuice/
├── .github/workflows/     # CI/CD (auto-deploy, PR checks)
├── articles/              # Blog posts (9 articles)
├── products/              # Product detail pages (6 products)
├── css/style.css          # All styles (single file)
├── js/main.js             # SMS order builder, UI interactions
├── outputs/images/        # Product/hero images
├── generated_images/      # AI-generated images + logo
├── index.html             # Homepage
├── shop.html              # Product listing + order buttons
├── about.html             # Brand story
├── science.html           # Research/science page
├── blog.html              # Article listing
├── contact.html           # Order form + FAQ
├── partnerships.html      # B2B partnership tiers
├── 404.html               # Custom 404 page
├── sitemap.xml            # SEO sitemap
├── robots.txt             # SEO robots file
├── manifest.json          # PWA manifest
├── sw.js                  # Service worker
├── CNAME                  # Custom domain
└── .nojekyll              # Disables Jekyll processing
```

## SMS Order System

The order flow:
1. Customer picks product + size on shop.html or contact.html
2. Clicks "Order via Text" / "Send Text Order"
3. Native SMS app opens with pre-filled message:
   ```
   Hi! I'd like to order:
   Beetroid — 500ml $5.99
   Could you let me know availability and delivery? Thanks!
   ```
4. You receive the text, confirm availability, send invoice

**Phone:** 0434 694 141 (stored in `js/main.js` as `PHONE_NUMBER`)

## Adding a New Article

1. Create `articles/your-article.html` using an existing article as template
2. Add meta description, Open Graph tags, Plausible script, favicon
3. Add link in `blog.html`
4. Add entry to `sitemap.xml`
5. Commit and push

## Adding a New Product

1. Create `products/your-product.html` using an existing product as template
2. Add product card to `index.html` and `shop.html`
3. Add entry to `sitemap.xml`
4. Commit and push

## Common Tasks

### Update Phone Number
Edit `js/main.js`, change `PHONE_NUMBER` value. It's used everywhere.

### Update Pricing
Edit `js/main.js` → `getPriceForSize()` function. Also update displayed prices in HTML.

### Add Analytics Event
Plausible tracks pageviews automatically. For custom events:
```javascript
plausible('Event Name', { prop: 'value' });
```

## Troubleshooting

**Site not updating after push?**
- Check GitHub Actions tab for build errors
- Wait 2-3 minutes for propagation
- Clear browser cache (Ctrl+Shift+R)

**Broken links?**
- Run the PR check workflow or test locally
- All internal links should be relative (e.g., `shop.html`, `../index.html`)

**Images not loading?**
- Check file paths are correct relative to the HTML file
- Images are in `/outputs/images/` and `/generated_images/`

**SMS links not working?**
- Test on a real phone (desktop browsers may not handle `sms:` links)
- iOS and Android both supported
