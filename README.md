# Station House Physio

A responsive website built with plain HTML, CSS, and JavaScript. All website files are in `dist/`; no installation or build step is required.

## Preview

Open `dist/index.html` directly, or run `python -m http.server 8080 --directory dist` and visit http://localhost:8080.

## Included

- Responsive navigation and accessible mobile menu
- Treatment details in keyboard-accessible dialogs
- About, recovery approach, first visit, and FAQ sections
- Appointment enquiry download with date validation
- Privacy information and reduced-motion support

## Before the clinic launches

The existing domain could not be verified during development. The service descriptions and about copy are proposed content for the clinic to review, not verified statements of current provision. No staff credentials, prices, address, phone number, testimonials, or performance claims have been invented.

Connect a verified booking provider by replacing the `[data-book]` link and handler, and update the other booking links if direct scheduling is preferred. The current enquiry tool explicitly explains that it is not connected and does not book or transmit an appointment. Add verified contact details, confirmed services, clinic-specific privacy information, and any required patient-facing policies before public launch.

Photographs are illustrative Unsplash images, not photographs of the clinic or its staff. Fonts load from Google Fonts. Both require an internet connection; the layout includes system font fallbacks.

Upload the contents of `dist/` to the domain's web root to host this as a static site. Domain and DNS configuration are separate from the source code.
