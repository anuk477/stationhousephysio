const menuToggle = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navigation');
function closeMenu() {
  navigation.classList.remove('is-open');
  menuToggle.setAttribute('aria-expanded', 'false');
  menuToggle.setAttribute('aria-label', 'Open navigation');
}
menuToggle.addEventListener('click', () => {
  const open = menuToggle.getAttribute('aria-expanded') !== 'true';
  navigation.classList.toggle('is-open', open);
  menuToggle.setAttribute('aria-expanded', String(open));
  menuToggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
});
navigation.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => { if (event.key === 'Escape') closeMenu(); });
document.addEventListener('click', event => {
  if (!event.target.closest('.header')) closeMenu();
});
window.matchMedia('(min-width: 681px)').addEventListener('change', closeMenu);

function openDialog(dialog) {
  dialog.showModal();
  document.body.classList.add('modal-open');
}
document.querySelectorAll('dialog').forEach(dialog => {
  dialog.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => {
    if (!document.querySelector('dialog[open]')) document.body.classList.remove('modal-open');
  });
  dialog.addEventListener('click', event => {
    const bounds = dialog.getBoundingClientRect();
    if (event.target === dialog && (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom)) dialog.close();
  });
});
const treatments = {
  physio: { title: 'Physiotherapy', description: 'A starting point for understanding discomfort, stiffness, or changes in how you move. Your assessment explores your symptoms and how they affect your everyday life.', items: ['A conversation about your symptoms and goals', 'A movement and function assessment', 'Discussion of suitable treatment options', 'Individual exercise and self-management advice'], appointment: 0 },
  sports: { title: 'Sports injury rehabilitation', description: 'A progressive approach to recovering from injury and working towards the demands of your sport, whether you’re an occasional participant or a regular competitor.', items: ['Assessment of your injury and sporting demands', 'A progressive strength and movement programme', 'Guidance on managing your training load', 'Review of your readiness to return to activity'], appointment: 1 },
  postop: { title: 'Post-operative rehabilitation', description: 'Support for rebuilding movement, strength, and confidence following surgery. Your plan should take account of your procedure and the guidance from your surgical team.', items: ['Review of your surgical team’s recommendations', 'Appropriate movement and strengthening exercises', 'A staged plan towards everyday activities', 'Progress reviews as your recovery develops'], appointment: 2 },
  movement: { title: 'Movement & wellbeing', description: 'A practical approach to feeling more comfortable and confident in everyday movement, shaped around your starting point and the activities you enjoy.', items: ['Discussion of your movement goals', 'Assessment of strength, balance, and mobility', 'Exercises suited to your current abilities', 'Support with building a manageable routine'], appointment: 3 }
};
const treatmentDialog = document.querySelector('#treatment-dialog');
document.querySelectorAll('[data-treatment]').forEach(button => {
  button.addEventListener('click', () => {
    const treatment = treatments[button.dataset.treatment];
    document.querySelector('#treatment-title').textContent = treatment.title;
    document.querySelector('#treatment-description').textContent = treatment.description;
    document.querySelector('#treatment-list').replaceChildren(...treatment.items.map(item => {
      const li = document.createElement('li'); li.textContent = item; return li;
    }));
    document.querySelector('#appointment').selectedIndex = treatment.appointment;
    openDialog(treatmentDialog);
  });
});
document.querySelector('#treatment-book').addEventListener('click', () => treatmentDialog.close());
document.querySelector('[data-book]').addEventListener('click', event => {
  event.preventDefault();
  document.querySelector('#booking-status').textContent = '';
  openDialog(document.querySelector('#booking-dialog'));
});
document.querySelector('[data-privacy]').addEventListener('click', () => openDialog(document.querySelector('#privacy-dialog')));
const dateInput = document.querySelector('#preferred-date');
function localDate(date) {
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
}
dateInput.min = localDate(new Date());
document.querySelector('#booking-form').addEventListener('submit', event => {
  event.preventDefault();
  dateInput.min = localDate(new Date());
  if (!event.currentTarget.reportValidity()) return;
  const values = new FormData(event.currentTarget);
  const formattedDate = new Intl.DateTimeFormat('en-GB', { dateStyle: 'long' }).format(new Date(`${values.get('date')}T12:00:00`));
  const enquiry = `Station House Physio — Appointment enquiry\n\nAppointment: ${values.get('appointment')}\nPreferred date: ${formattedDate}\nPreferred time: ${values.get('time')}\n\nPlease contact me to discuss availability.\n\nThis is an enquiry, not a confirmed booking. Please send it to the clinic using verified contact details.\n`;
  const url = URL.createObjectURL(new Blob([enquiry], { type: 'text/plain;charset=utf-8' }));
  const link = document.createElement('a');
  link.href = url; link.download = 'station-house-appointment-enquiry.txt';
  document.body.append(link); link.click(); link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
  document.querySelector('#booking-status').textContent = 'Your enquiry has been downloaded. Send it to the clinic using its verified contact details. No appointment has been booked.';
});
document.querySelector('#year').textContent = new Date().getFullYear();
