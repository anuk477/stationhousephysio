const menuToggle = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navigation');
const treatmentsDropdown = document.querySelector('.nav-treatments');
const desktopHover = window.matchMedia('(any-hover: hover) and (min-width: 681px)');
let dropdownCloseTimer;
function cancelDropdownClose() {
  clearTimeout(dropdownCloseTimer);
}
treatmentsDropdown.addEventListener('pointerenter', event => {
  if (event.pointerType !== 'mouse' || !desktopHover.matches) return;
  cancelDropdownClose();
  treatmentsDropdown.open = true;
});
treatmentsDropdown.addEventListener('pointerleave', event => {
  if (event.pointerType !== 'mouse' || !desktopHover.matches) return;
  cancelDropdownClose();
  dropdownCloseTimer = setTimeout(() => {
    if (!treatmentsDropdown.matches(':focus-within')) treatmentsDropdown.open = false;
  }, 250);
});
treatmentsDropdown.addEventListener('focusin', cancelDropdownClose);
function closeMenu() {
  cancelDropdownClose();
  treatmentsDropdown.open = false;
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
document.addEventListener('keydown', event => {
  if (event.key !== 'Escape') return;
  cancelDropdownClose();
  if (treatmentsDropdown.open) {
    treatmentsDropdown.open = false;
    treatmentsDropdown.querySelector('summary').focus();
  } else if (navigation.classList.contains('is-open')) {
    closeMenu();
    menuToggle.focus();
  }
});
document.addEventListener('click', event => {
  if (!event.target.closest('.nav-treatments')) treatmentsDropdown.open = false;
  if (!event.target.closest('.header')) closeMenu();
});
treatmentsDropdown.addEventListener('focusout', event => {
  if (!treatmentsDropdown.contains(event.relatedTarget)) treatmentsDropdown.open = false;
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
const appointmentSelect = document.querySelector('#appointment');
const defaultAppointment = Number(document.body.dataset.defaultAppointment);
if (Number.isInteger(defaultAppointment) && defaultAppointment >= 0 && defaultAppointment < appointmentSelect.options.length) {
  appointmentSelect.selectedIndex = defaultAppointment;
}
document.querySelectorAll('[data-book]').forEach(link => {
  link.addEventListener('click', event => {
    event.preventDefault();
    document.querySelector('#booking-status').textContent = '';
    openDialog(document.querySelector('#booking-dialog'));
  });
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
