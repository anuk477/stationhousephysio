# Station House Physio

A responsive website built with plain HTML, CSS, and JavaScript. All website files are in `dist/`; no installation or build step is required.

## Preview

Run `python -m http.server 8080 --directory dist` and visit http://localhost:8080.

## Included

- Responsive navigation and accessible mobile menu
- 13 dedicated treatment pages with overviews, FAQs, and treatment-specific enquiry buttons
- About, recovery approach, first visit, and FAQ sections
- A dedicated /booking page with name, preferred date and time, treatment selection, optional notes, and a request download
- Privacy information and reduced-motion support

## Before the clinic launches

The existing domain could not be verified during development. The service descriptions and about copy are proposed content for the clinic to review, not verified statements of current provision. No staff credentials, prices, address, phone number, testimonials, or performance claims have been invented.

Connect a verified booking provider or backend to the booking form in `dist/booking/index.html` and replace its local download handler in `dist/script.js` to accept live requests. The current enquiry tool explicitly explains that it is not connected and does not book or transmit an appointment. Add verified contact details, confirmed services, clinic-specific privacy information, and any required patient-facing policies before public launch.

Photographs are illustrative Unsplash images, not photographs of the clinic or its staff. Fonts load from Google Fonts. Both require an internet connection; the layout includes system font fallbacks.

Upload the contents of `dist/` to the domain's web root to host this as a static site. Domain and DNS configuration are separate from the source code.

## Treatment pages

Every treatment has a static HTML page in `dist/treatments/`. Homepage cards link directly to these pages and work without JavaScript. To update page content or regenerate the pages, edit `scripts/build-treatment-pages.py` and run `python scripts/build-treatment-pages.py`. The script reuses the homepage header and footer, and also generates the booking page. Clinical overviews include links to public patient information; the clinic should review its own service descriptions before public launch.

The `/booking` route uses `dist/booking/index.html` (a static server may redirect to `/booking/`). Treatment links preselect the treatment with a public slug in the query string. Name and notes are never placed in the URL or browser storage. No patient information is transmitted; downloads happen locally. The submission button is disabled without JavaScript to prevent an unintended form submission.

## Prices

The `/prices` page is generated from `content/prices.json`. The 19 physiotherapy entries, session lengths, and fees were matched to https://footandanklecentre.co.uk/prices/ on 17 November 2026. Services without a separate price on that reference are not assigned an invented fee. Regenerate all pages with `python scripts/build-treatment-pages.py` after editing the schedule.
