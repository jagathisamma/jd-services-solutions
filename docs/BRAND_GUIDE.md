# JD Services & Solutions — Brand & UI Guide

## Brand identity
- Name: JD Services & Solutions
- Tagline: **Service Today... Smile Tomorrow...**
- Service location: Erode, Tamil Nadu
- Public contact: 8940454260 (Call & WhatsApp)

## Official visual references
The owner supplied an official transparent JD Services & Solutions logo and a vertical service poster on 21 November 2026. The logo is the canonical identity asset. Use the original asset unchanged, preserve its transparent background and aspect ratio, and never recreate it with text, CSS, AI, or a substitute mark. The poster is a composition reference, not a template to copy literally.

## Color system
Canonical values live in `data/config/brand.yml`.

| Token | Hex | Use |
|---|---|---|
| Navy | `#071D55` | Primary brand surface, header/footer, strong text |
| Royal/electric blue | `#075BD8` | Secondary action, links, interactive states |
| Orange | `#FF6A00` | Primary CTA and selected emphasis |
| Yellow | `#FFC400` | Small highlights, focus accents, tagline emphasis |
| White | `#FFFFFF` | Text and clean contrast surfaces |

### Usage rules
- Navy is the visual anchor. Avoid making every section a different saturated gradient.
- Orange is the main conversion accent; use consistently for the primary action.
- Blue is for secondary actions, links, selected states and informational emphasis.
- Yellow is a highlight, not a paragraph or large-area background color.
- Use white or near-white content surfaces where they improve long-form readability.
- Check WCAG contrast for actual foreground/background pairs; do not infer accessibility from brand colors alone.

## Typography
Use a high-quality system font stack by default. Do not block first paint on remote font CSS. Add a self-hosted font only when there is a measured benefit and licensing is clear. Use a restrained type scale, strong heading hierarchy, readable line lengths and comfortable Tamil glyph rendering.

## Layout and interaction
- Mobile-first, responsive at 360, 390, 430, 768 and 1280 CSS px.
- Consistent spacing scale, radii, borders and elevation.
- Large touch targets; visible keyboard focus; reduced-motion support.
- Keep call/WhatsApp actions obvious without covering page content.
- Service cards must explain the service in plain language and route to a relevant enquiry.
- Use real operational claims only. Explain pickup/onsite availability as subject to location and confirmation.

## Photography and assets
- Prefer real, owner-approved workshop and service photographs.
- Do not use generated technician imagery as proof of JD staff, credentials or completed work.
- Provide width/height or aspect-ratio hints, modern formats and responsive sizing.
- Lazy-load below-the-fold imagery; do not lazy-load the primary LCP image.
- Use meaningful alt text; decorative imagery gets empty alt text.

## Product design standard
The public website, campaign pages and future owner Admin must share the same design tokens, typography, components, accessibility rules and content contracts. Admin is a private operational application, not a hidden static page. No fake login, localStorage-only CRM or client-side secrets.

## Source of truth
- Tokens: `data/config/brand.yml`
- Business/service records: `data/config/site.yml` and `data/records/services.json`
- Product architecture: `docs/ARCHITECTURE.md`
- Delivery principles: `docs/OPERATING_MODEL.md`
