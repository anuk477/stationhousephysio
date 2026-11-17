const menuToggle = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navigation');
const treatmentsDropdown = document.querySelector('.nav-treatments');
const desktopHover = window.matchMedia('(any-hover: hover) and (min-width: 961px)');
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
window.matchMedia('(min-width: 961px)').addEventListener('change', closeMenu);

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
document.querySelector('[data-privacy]').addEventListener('click', () => openDialog(document.querySelector('#privacy-dialog')));

function localDate(date) {
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
}
const bookingForm = document.querySelector('#booking-form');
if (bookingForm) {
  const appointmentSelect = document.querySelector('#appointment');
  const dateInput = document.querySelector('#preferred-date');
  const nameInput = document.querySelector('#patient-name');
  const requestedTreatment = new URLSearchParams(window.location.search).get('treatment');
  if ([...appointmentSelect.options].some(option => option.value === requestedTreatment)) {
    appointmentSelect.value = requestedTreatment;
  }
  dateInput.min = localDate(new Date());
  dateInput.addEventListener('focus', () => { dateInput.min = localDate(new Date()); });
  nameInput.addEventListener('input', () => nameInput.setCustomValidity(''));
  bookingForm.addEventListener('input', () => {
    document.querySelector('#booking-status').textContent = '';
  });
  bookingForm.addEventListener('submit', event => {
    event.preventDefault();
    dateInput.min = localDate(new Date());
    nameInput.setCustomValidity(nameInput.value.trim() ? '' : 'Please enter your name.');
    if (!bookingForm.reportValidity()) return;
    const values = new FormData(bookingForm);
    const formattedDate = new Intl.DateTimeFormat('en-GB', { dateStyle: 'long' }).format(new Date(`${values.get('date')}T12:00:00`));
    const treatment = appointmentSelect.selectedOptions[0].textContent;
    const notes = String(values.get('notes') || '').trim();
    const request = [
      'Station House Physio — Appointment request',
      '',
      `Name: ${String(values.get('name')).trim()}`,
      `Treatment: ${treatment}`,
      `Preferred date: ${formattedDate}`,
      `Preferred time: ${values.get('time')}`,
      `Notes: ${notes || 'None provided'}`,
      '',
      'This is a request, not a confirmed appointment.',
      'Send this request to the clinic using verified contact details. The clinic must confirm availability.',
      ''
    ].join('\n');
    const url = URL.createObjectURL(new Blob([request], { type: 'text/plain;charset=utf-8' }));
    const link = document.createElement('a');
    link.href = url;
    link.download = 'station-house-appointment-request.txt';
    document.body.append(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    document.querySelector('#booking-status').textContent = 'Your appointment request has been downloaded. Send it to the clinic using its verified contact details. Your appointment is not confirmed yet.';
  });
  document.querySelector('#booking-submit').disabled = false;
}
document.querySelector('#year').textContent = new Date().getFullYear();
