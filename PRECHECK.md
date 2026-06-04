# Site safety checks — run before each deploy

## Pre-Deploy Checklist

### 1. Link Validation
- All internal href references point to existing files
- No broken article or product page links

### 2. SEO Baseline
- Every HTML page has meta description
- sitemap.xml exists and lists all pages
- robots.txt exists

### 3. Analytics
- Every HTML page includes Plausible script
- data-domain is set to glengalafresh.au

### 4. Branding
- Every HTML page has favicon link
- Phone number is consistent (61434694141)

### 5. SMS Order System
- js/main.js has PHONE_NUMBER variable
- Order buttons have data-wa-product attribute
- Size buttons have data-size and data-price attributes

### 6. Required Files
- sitemap.xml, robots.txt, 404.html, .nojekyll, CNAME, manifest.json, sw.js
