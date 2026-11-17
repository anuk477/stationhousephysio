"""Generate the static treatment pages. Run from the project root."""
from pathlib import Path
from html import escape
import re
import json

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
NHS = ('NHS: Physiotherapy', 'https://www.nhs.uk/tests-and-treatments/physiotherapy/')
TREATMENTS = [
    ('physio', 'physiotherapy', 'Physiotherapy', 0,
     'Understand your movement. Find your way forward.',
     'Physiotherapy begins with understanding how your symptoms affect your movement and everyday life. An assessment can help you explore the next steps towards your own goals.',
     'Your physiotherapist may assess movement, strength, and balance, alongside a conversation about your health history. Your plan may include exercise, hands-on treatment, and advice on managing symptoms.',
     ['Your symptoms and how they affect your day', 'Movement, strength, and everyday activities', 'A practical plan with agreed goals'],
     'Do I need to choose a technique first?', 'No. An initial assessment is a place to discuss your concerns and explore suitable options together.', NHS),
    ('sports', 'sports-injury-rehabilitation', 'Sports Injury Rehabilitation', 1,
     'A considered return to the activity you love.',
     'Your sport is personal. Your rehabilitation should take account of the activity you enjoy, your current starting point, and what you want to return to.',
     'Bring details of your injury, training routine, and any previous assessments. Your appointment is a chance to discuss a progressive plan and how to review it against the demands of your sport.',
     ['The demands of your sport or training', 'Your current movement and activity tolerance', 'Goals for a gradual return to participation'],
     'When can I return to sport?', 'There is no single timeline. Your physiotherapist can discuss what needs to be assessed and how progress will be reviewed before you increase activity.', NHS),
    ('postop', 'post-operative-rehabilitation', 'Post-operative Rehabilitation', 2,
     'Your recovery. A clear next step.',
     'Rehabilitation after surgery needs to reflect your procedure and the guidance of your surgical team. Start with a conversation about your recovery so far and the activities that matter to you.',
     'Bring your discharge information and any rehabilitation instructions. These help your physiotherapist discuss an appropriate plan, including what you have already been advised to do or avoid.',
     ['Your procedure and surgical team’s instructions', 'Your current abilities and everyday needs', 'A staged plan and opportunities to review progress'],
     'What information should I bring?', 'Bring your discharge summary, rehabilitation protocol if provided, and details of any restrictions or follow-up appointments.', NHS),
    ('movement', 'movement-and-wellbeing', 'Movement & Wellbeing', 3,
     'Make more room for everyday movement.',
     'Everyday movement means different things to different people. This appointment gives you space to discuss comfort, confidence, and the activities you would like to make part of your routine.',
     'Your starting point matters more than a particular level of fitness. Talk through your schedule, preferences, and any barriers so the next steps can be shaped around your life.',
     ['Activities you enjoy or want to try', 'A starting point that suits your circumstances', 'Manageable goals and regular reflection'],
     'Do I need to be fit already?', 'No. Explain where you are starting from and what you hope to work towards so you can discuss an appropriate plan.', NHS),
    ('shockwave', 'shockwave-therapy', 'Shockwave Therapy', 4,
     'Explore whether shockwave fits your care.',
     'Shockwave therapy uses a device to deliver sound waves through the skin to a selected area. It is an option used for some persistent tendon and related soft-tissue problems.',
     'An assessment comes first. Your physiotherapist can explain why it may or may not suit your symptoms, what treatment feels like, and how it relates to your wider rehabilitation plan.',
     ['An assessment before treatment is considered', 'Discussion of suitability and alternatives', 'An explanation of sensations, risks, and follow-up'],
     'Is shockwave suitable for everyone?', 'No. The clinician needs to review your symptoms and health history before recommending it. Ask about the expected benefits, limitations, and risks for your situation.',
     ('Royal National Orthopaedic Hospital: Shockwave therapy', 'https://www.rnoh.nhs.uk/patients-and-visitors/patient-information-guides/radial-extracorporeal-shockwave-therapy-eswt')),
    ('myofascial', 'myofascial-release', 'Myofascial Release', 5,
     'A hands-on approach, discussed with you.',
     'Myofascial release is a form of hands-on soft-tissue work using sustained pressure. It focuses on the muscles and the connective tissue around them.',
     'Your appointment starts with the areas that concern you and how they affect your day. Discuss the proposed technique, your comfort preferences, and how any hands-on work fits into a wider plan.',
     ['Your symptoms and movement goals', 'An explanation of the proposed hands-on approach', 'Pressure and positioning discussed with you'],
     'Can I ask for the pressure to be changed?', 'Yes. Tell your physiotherapist what feels comfortable and ask to pause or stop at any time.',
     ('Cleveland Clinic: Myofascial release', 'https://my.clevelandclinic.org/health/treatments/24011-myofascial-release-therapy')),
    ('triggerpoint', 'triggerpoint-therapy', 'Triggerpoint Therapy', 6,
     'Focused attention. A wider view of your movement.',
     'Manual triggerpoint therapy involves applying pressure to tender areas in muscles. It is one approach to discuss after assessing your symptoms and movement.',
     'Tenderness alone does not explain the whole picture. Your physiotherapist can discuss what they find, the uncertainty around treatment effects, and how to judge whether the agreed approach is useful for you.',
     ['Assessment of tenderness alongside movement', 'Discussion of pressure and your comfort', 'Review against goals that matter to you'],
     'Does triggerpoint therapy mean injections?', 'This page describes a manual pressure approach. Ask your clinician to explain the exact technique they propose before agreeing to treatment.',
     ('Chartered Society of Physiotherapy: Trigger points', 'https://www.csp.org.uk/frontline/article/hot-topic-trigger-points-myth-or-magic')),
    ('exercise', 'exercise-rehabilitation', 'Exercise Rehabilitation', 7,
     'Practical movement. Personal progress.',
     'Exercise rehabilitation uses a programme of movement tailored to your assessment and goals. Exercises may focus on mobility, strength, balance, or the activities you want to return to.',
     'The plan should make sense in your routine. Talk about the time, space, and equipment available to you, and ask for clear explanations before practising independently.',
     ['Goals linked to everyday life or activity', 'Clear demonstrations and a chance to practise', 'A plan to review and adapt your programme'],
     'Will I need gym equipment?', 'Tell your physiotherapist what equipment and space you have. You can then discuss a programme that fits your circumstances.', NHS),
    ('electrotherapy', 'electrotherapy', 'Electrotherapy', 8,
     'Understand the options before you decide.',
     'Electrotherapy is a broad term for treatments using electrical or other physical energy. Examples used in physiotherapy include TENS and therapeutic ultrasound, which work in different ways.',
     'Ask which specific treatment is being proposed, why it is being considered, and what evidence supports it for your symptoms. Equipment-based treatment should be discussed in the context of your overall care.',
     ['Clarification of the device and proposed treatment', 'A review of suitability and health history', 'Discussion of expected effects and alternatives'],
     'Are all types of electrotherapy the same?', 'No. Different devices have different uses and considerations. Confirm which type is available and suitable during your assessment.', NHS),
    ('dryneedling', 'dry-needling', 'Dry Needling', 9,
     'Time to understand a needle-based option.',
     'Dry needling involves inserting fine needles into selected tissues, often muscles, without injecting medication. Whether it is appropriate depends on an individual assessment.',
     'Before deciding, discuss the proposed treatment area, possible benefits, limitations, and risks with your clinician. You can ask about non-needle alternatives and take time to make your choice.',
     ['Assessment and a discussion of your preferences', 'Explanation of the proposed technique and risks', 'Consent before any treatment begins'],
     'Is dry needling the same as acupuncture?', 'Both use fine needles, but the approach and rationale can differ. Ask your clinician which technique they propose and why.',
     ('NHS Fife: Acupuncture and dry needling', 'https://www.nhsfife.org/services/all-services/patient-advice/acupuncturedry-needling/')),
    ('cupping', 'cupping-therapy', 'Cupping Therapy', 10,
     'An informed choice about your treatment.',
     'Cupping uses cups to create suction on the skin. Research into its benefits is limited, so it is worth discussing the evidence and alternatives before choosing it.',
     'Cupping can leave temporary skin marks and may have other side effects. Ask which type is proposed, how your skin and health history will be assessed, and whether another approach would better suit your goals.',
     ['A discussion of the evidence and its limitations', 'Review of your skin, health history, and suitability', 'Explanation of marks, other risks, and aftercare'],
     'Will cupping leave marks?', 'Temporary marks are common. Discuss this and other possible effects with your clinician before treatment, including any concerns about your skin.',
     ('National Center for Complementary and Integrative Health: Cupping', 'https://www.nccih.nih.gov/health/cupping')),
    ('acupuncture', 'acupuncture', 'Acupuncture', 11,
     'Explore acupuncture with clear information.',
     'Acupuncture involves inserting fine needles at selected points on the body. Evidence and suitability vary depending on the condition being treated.',
     'Your assessment is an opportunity to ask why acupuncture is being considered, what the alternatives are, and what benefits and risks are relevant to you. Your preferences should be part of that discussion.',
     ['Discussion of your symptoms and health history', 'An explanation of the approach and alternatives', 'Time for questions and consent before treatment'],
     'Can I choose an approach without needles?', 'Yes. Tell your physiotherapist about your preferences so you can discuss other suitable options together.',
     ('NCCIH: Acupuncture effectiveness and safety', 'https://www.nccih.nih.gov/health/acupuncture-effectiveness-and-safety')),
    ('massage', 'sports-massage', 'Sports Massage', 12,
     'Make time for a conversation about muscle care.',
     'Sports massage is a form of soft-tissue treatment associated with sport and physical activity. The approach and pressure should be discussed around your needs and comfort.',
     'Share your activity routine, the areas that concern you, and any recent injury. Your clinician can explain whether massage is appropriate or whether an assessment or different approach would be a better starting point.',
     ['Your activity routine and treatment goals', 'An explanation of the areas and techniques proposed', 'Ongoing communication about comfort and pressure'],
     'Should I mention an injury before the session?', 'Yes. Explain any recent injury, symptoms, or health concerns before treatment so your clinician can discuss suitability and next steps.',
     ('Healthdirect: Sports massage', 'https://www.healthdirect.gov.au/treatments-and-self-care/sports-massage')),
]

home_path = DIST / 'index.html'
home = home_path.read_text(encoding='utf-8')
slug_by_key = {row[0]: row[1] for row in TREATMENTS}

def card_to_link(match):
    classes, key, contents = match.groups()
    return f'<a class="{classes}" href="treatments/{slug_by_key[key]}.html">{contents}</a>'

home = re.sub(r'<button class="(treatment-card|specialist-treatment)" data-treatment="([^"]+)">(.*?)</button>', card_to_link, home, flags=re.S)
home = re.sub(r'  <dialog id="treatment-dialog".*?</dialog>\s*', '', home, flags=re.S)
home = re.sub(r'<dialog id="booking-dialog".*?</dialog>\s*', '', home, flags=re.S)
home = home.replace('href="#" data-book', 'href="booking/"')
home = home.replace('href="#booking"', 'href="booking/"')
dropdown_links = ''.join(
    f'<a href="treatments/{row[1]}.html">{escape(row[2])}<span aria-hidden="true">↗</span></a>'
    for row in TREATMENTS
)
dropdown = (
    '<details class="nav-treatments"><summary>Treatments '
    '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="m4 6 4 4 4-4" stroke="currentColor" stroke-width="1.5"/></svg>'
    '</summary><div class="treatments-dropdown"><p class="eyebrow">FIND YOUR WAY FORWARD</p>'
    '<div class="dropdown-treatment-links">' + dropdown_links + '</div>'
    '<a class="dropdown-all" href="#treatments">View all treatments <span aria-hidden="true">→</span></a>'
    '</div></details>'
)
if '<details class="nav-treatments">' in home:
    home = re.sub(r'<details class="nav-treatments">.*?</details>', lambda _: dropdown, home, count=1, flags=re.S)
else:
    home = home.replace('<a href="#treatments">Treatments</a>', dropdown, 1)
if '<a href="prices/">Prices</a>' not in home:
    home = home.replace('<a href="#faqs">FAQs</a>', '<a href="prices/">Prices</a><a href="#faqs">FAQs</a>', 1)
    home = home.replace('<a href="booking/">Book now</a>', '<a href="prices/">Prices</a><a href="booking/">Book now</a>', 1)
home_path.write_text(home, encoding='utf-8')
head = home.split('<head>')[1].split('</head>')[0]
header = home.split('<body>')[1].split('  <main id="main">')[0]
footer = home.split('  <footer')[1].split('</body>')[0]
footer = '  <footer' + footer

def page_links(fragment):
    fragment = re.sub(r'href="#(home|treatments|about|approach|faqs|first-visit)"', r'href="../index.html#\1"', fragment)
    return fragment.replace('href="booking/', 'href="../booking/').replace('href="prices/', 'href="../prices/')

out = DIST / 'treatments'
out.mkdir(exist_ok=True)
for key, slug, title, appointment, tagline, intro, overview, points, question, answer, source in TREATMENTS:
    e = escape
    page_head = re.sub(r'<title>.*?</title>', f'<title>{e(title)} | Station House Physio</title>', head)
    page_head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{e(intro, quote=True)}">', page_head)
    page_head = page_head.replace('href="styles.css"', 'href="../styles.css"').replace('src="script.js"', 'src="../script.js"')
    nav = ''.join(f'<a href="{other[1]}.html"'+(' aria-current="page"' if other[0] == key else '')+f'>{e(other[2])}<span aria-hidden="true">↗</span></a>' for other in TREATMENTS)
    bullets = ''.join(f'<li>{e(point)}</li>' for point in points)
    page_header = page_links(header)
    page_header = page_header.replace('href="treatments/', 'href="')
    page_header = page_header.replace(f'href="{slug}.html"', f'href="{slug}.html" aria-current="page"')
    page = f'''<!doctype html>
<html lang="en-GB">
<head>{page_head}</head>
<body data-default-appointment="{appointment}">
{page_header}
  <main id="main">
    <div class="wrap"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a><span aria-hidden="true">/</span><a href="../index.html#treatments">Treatments</a><span aria-hidden="true">/</span><span aria-current="page">{e(title)}</span></nav></div>
    <section class="treatment-hero"><div class="wrap treatment-hero-grid"><div><p class="eyebrow">CARE THAT MOVES WITH YOU</p><h1>{e(title)}</h1><p class="treatment-tagline serif">{e(tagline)}</p><p class="treatment-intro">{e(intro)}</p><a class="button" href="#booking" data-book>Enquire about this treatment <span aria-hidden="true">↗</span></a></div><aside class="treatment-at-a-glance" aria-label="Your care at a glance"><p class="eyebrow">YOUR CARE, YOUR CHOICE</p><h2>A personal<br><span class="serif">starting point.</span></h2><ul><li>Start with an assessment</li><li>Discuss your options</li><li>Agree the next step together</li></ul><p>Suitability, treatment details, and availability can be discussed with the clinic before you proceed.</p></aside></div></section>
    <div class="wrap treatment-page-grid">
      <div class="treatment-content">
        <section aria-labelledby="overview-title"><p class="eyebrow">UNDERSTANDING YOUR OPTIONS</p><h2 id="overview-title">What is involved?</h2><p>{e(overview)}</p></section>
        <section aria-labelledby="appointment-title"><h2 id="appointment-title">What to expect</h2><p>Your appointment is a chance to ask questions, share your priorities, and understand the proposed approach.</p><ul class="treatment-checklist">{bullets}</ul></section>
        <section class="treatment-prepare" aria-labelledby="prepare-title"><h2 id="prepare-title">Before your visit</h2><p>Wear comfortable clothing and bring any relevant referral letters, scan reports, or instructions from another healthcare professional. Make a note of the questions you would like to ask.</p></section>
        <section aria-labelledby="questions-title"><h2 id="questions-title">Your questions, answered.</h2><div class="faq-list treatment-page-faq"><details open><summary>{e(question)}<span aria-hidden="true">+</span></summary><p>{e(answer)}</p></details><details><summary>How many sessions will I need?<span aria-hidden="true">+</span></summary><p>The plan depends on your assessment, goals, and response. Discuss a review point with your physiotherapist rather than assuming a fixed number of visits.</p></details><details><summary>How do I make an enquiry?<span aria-hidden="true">+</span></summary><p>Use the enquiry button on this page to prepare a request with this treatment selected. Online booking is not connected yet, so a downloaded enquiry does not reserve an appointment.</p></details></div></section>
        <details class="further-reading"><summary>Further reading</summary><p>For general background: <a href="{e(source[1], quote=True)}" target="_blank" rel="noopener noreferrer">{e(source[0])} <span aria-hidden="true">↗</span></a>. This information does not replace an individual assessment.</p></details>
      </div>
      <aside class="treatment-sidebar"><h2>Explore treatments</h2><nav aria-label="Other treatments">{nav}</nav><a class="text-link" href="../index.html#treatments">Back to all treatments <span aria-hidden="true">←</span></a></aside>
    </div>
    <section class="booking-section wrap" id="booking"><div class="booking-panel"><div><p class="eyebrow">YOUR NEXT STEP</p><h2>Let’s talk about<br><span class="serif">what matters to you.</span></h2><p>Start with your goals. Explore your options together.</p></div><a class="button button-light" href="#booking" data-book>Enquire about {e(title)} <span aria-hidden="true">↗</span></a></div></section>
  </main>
{page_links(footer)}
</body>
</html>
'''
    page = page.replace('href="#booking" data-book', 'href="../booking/"')
    page = page.replace('href="../booking/"', f'href="../booking/?treatment={slug}"')
    page = page.replace('Use the enquiry button on this page to prepare a request with this treatment selected. Online booking is not connected yet, so a downloaded enquiry does not reserve an appointment.', 'The enquiry button opens our booking page with this treatment selected. Add your preferences and download your request. The clinic must confirm availability before an appointment is booked.')
    (out / f'{slug}.html').write_text(page, encoding='utf-8')

booking_head = re.sub(r'<title>.*?</title>', '<title>Book an Appointment | Station House Physio</title>', head)
booking_head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Plan your visit to Station House Physio. Choose a treatment and share your preferred appointment date and time.">', booking_head)
booking_head = booking_head.replace('href="styles.css"', 'href="../styles.css"').replace('src="script.js"', 'src="../script.js"')
booking_header = page_links(header).replace('href="treatments/', 'href="../treatments/')
booking_header = booking_header.replace('href="../booking/"', 'href="#booking-form" aria-current="page"')
booking_footer = page_links(footer).replace('href="../booking/"', 'href="#booking-form"')
options = ''.join(f'<option value="{escape(row[1])}">{escape(row[2])}</option>' for row in TREATMENTS)
booking_page = f'''<!doctype html>
<html lang="en-GB">
<head>{booking_head}</head>
<body>
{booking_header}
  <main id="main">
    <div class="wrap"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a><span aria-hidden="true">/</span><span aria-current="page">Booking</span></nav></div>
    <section class="booking-page wrap">
      <div class="booking-page-intro"><p class="eyebrow">LET’S GET YOU MOVING</p><h1>Your next step.<br><span class="serif">Made personal.</span></h1><p>Tell us what you’re looking for and when you’d prefer to visit.</p><div class="booking-explainer"><h2>A request, then a conversation.</h2><p>Your preferred date and time are a request, subject to availability. An appointment is only booked when the clinic confirms it.</p></div><a class="text-link" href="../index.html#treatments">Explore our treatments <span aria-hidden="true">↗</span></a></div>
      <div class="booking-form-card"><h2>Book an appointment</h2><p class="booking-form-description">Fields marked <span aria-hidden="true">*</span> are required.</p>
        <form id="booking-form" method="post">
          <label for="patient-name">Name <span aria-hidden="true">*</span></label><input id="patient-name" name="name" autocomplete="name" maxlength="120" required>
          <div class="form-row"><div><label for="preferred-date">Preferred date <span aria-hidden="true">*</span></label><input id="preferred-date" name="date" type="date" required></div><div><label for="preferred-time">Preferred time <span aria-hidden="true">*</span></label><input id="preferred-time" name="time" type="time" required></div></div>
          <label for="appointment">Treatment <span aria-hidden="true">*</span></label><select id="appointment" name="appointment" required><option value="">Please select a treatment</option>{options}</select>
          <label for="booking-notes">Notes <span class="optional-label">(optional)</span></label><textarea id="booking-notes" name="notes" rows="4" maxlength="2000" aria-describedby="notes-help" placeholder="Anything you’d like to ask before your visit?"></textarea><p class="form-hint" id="notes-help">A brief note is enough. Please avoid including detailed medical history.</p>
          <div class="booking-form-notice"><strong>Online submission is not connected yet.</strong><p>This form creates a request you can download and send to the clinic using its verified contact details. Your name and notes stay in this page until you download them; nothing is sent to the clinic.</p></div>
          <button class="button" type="submit" id="booking-submit" disabled>Download appointment request <span aria-hidden="true">↓</span></button><noscript><p>Please enable JavaScript to prepare and download your appointment request.</p></noscript><p id="booking-status" role="status" aria-atomic="true"></p>
        </form>
      </div>
    </section>
  </main>
{booking_footer}
</body>
</html>
'''
booking_dir = DIST / 'booking'
booking_dir.mkdir(exist_ok=True)
(booking_dir / 'index.html').write_text(booking_page, encoding='utf-8')

pricing = json.loads((ROOT / 'content' / 'prices.json').read_text(encoding='utf-8'))
prices_head = re.sub(r'<title>.*?</title>', '<title>Physiotherapy Prices | Station House Physio</title>', booking_head)
prices_head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Explore physiotherapy fees, session lengths, and treatment prices at Station House Physio, including a free 15-minute first consultation.">', prices_head)
prices_header = page_links(header).replace('href="treatments/', 'href="../treatments/')
prices_header = prices_header.replace('href="../prices/"', 'href="./" aria-current="page"')
prices_footer = page_links(footer).replace('href="../prices/"', 'href="./" aria-current="page"')
price_sections = []
for index, group in enumerate(pricing['groups']):
    rows = []
    for row in group['rows']:
        fee = 'Free' if row['price'] == 0 else f'£{row["price"]}'
        if row.get('extra'):
            fee = '+' + fee
        label = f'Enquire about {row["name"]}, {row["duration"]}'
        rows.append(f'<tr><th scope="row">{escape(row["name"])}</th><td>{escape(row["duration"])}</td><td class="price-fee">{fee}</td><td><a href="../booking/?treatment={row["treatment"]}" aria-label="{escape(label, quote=True)}">Enquire <span aria-hidden="true">↗</span></a></td></tr>')
    price_sections.append(f'<section class="price-group" aria-labelledby="price-group-{index}"><h2 id="price-group-{index}">{escape(group["title"])}</h2><p>{escape(group["description"])}</p><table class="price-table"><caption class="visually-hidden">{escape(group["title"])}</caption><thead><tr><th scope="col">Appointment</th><th scope="col">Duration</th><th scope="col">Fee</th><th scope="col"><span class="visually-hidden">Booking</span></th></tr></thead><tbody>{"".join(rows)}</tbody></table></section>')
prices_page = f'''<!doctype html>
<html lang="en-GB"><head>{prices_head}</head><body>
{prices_header}
<main id="main">
  <div class="wrap"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a><span aria-hidden="true">/</span><span aria-current="page">Prices</span></nav></div>
  <section class="prices-hero"><div class="wrap"><div><p class="eyebrow">PLAN YOUR CARE</p><h1>Clear prices.<br><span class="serif">A personal approach.</span></h1><p>Choose the time and treatment that fit your next step. All prices are in pounds sterling.</p></div><div class="first-consultation"><p class="eyebrow">LET’S START WITH A CONVERSATION</p><h2>First consultation</h2><div class="consultation-fee">Free <span>15 minutes</span></div><p>Time to discuss your concerns and explore the next steps.</p><a class="button" href="../booking/?treatment=physiotherapy">Plan your first visit <span aria-hidden="true">↗</span></a></div></div></section>
  <div class="wrap prices-content">{''.join(price_sections)}<section class="prices-help"><h2>Not sure which session to choose?</h2><p>Discuss your needs and the appropriate session length with the clinic before booking. Myofascial Release, Exercise Rehabilitation, and other services without a separate fee listed here can be discussed as part of that conversation.</p><p>Kinesiology Taping is an optional add-on, charged in addition to the appointment fee.</p><p class="prices-source">Prices matched to the <a href="{escape(pricing['source'], quote=True)}" target="_blank" rel="noopener noreferrer">Foot &amp; Ankle Centre physiotherapy fee schedule</a>, checked {escape(pricing['checked'])}. Confirm your appointment fee with the clinic before proceeding.</p></section></div>
  <section class="booking-section wrap"><div class="booking-panel"><div><p class="eyebrow">YOUR NEXT STEP</p><h2>Ready to<br><span class="serif">move forward?</span></h2><p>Choose your treatment and share your preferred date and time.</p></div><a class="button button-light" href="../booking/">Book an appointment <span aria-hidden="true">↗</span></a></div></section>
</main>
{prices_footer}
</body></html>'''
prices_dir = DIST / 'prices'
prices_dir.mkdir(exist_ok=True)
(prices_dir / 'index.html').write_text(prices_page, encoding='utf-8')
print(f'Generated {len(TREATMENTS)} treatment pages and updated homepage links.')
