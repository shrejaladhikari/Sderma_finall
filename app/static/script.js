const bookingModal = document.getElementById('bookingModal');

//  dermatologist data
bookingModal.addEventListener('show.bs.modal', function (event) {
  const button = event.relatedTarget;

  const id = button.getAttribute('data-id');
  const name = button.getAttribute('data-name');
  const expertise = button.getAttribute('data-expertise');
  const clinic = button.getAttribute('data-clinic');
  const location = button.getAttribute('data-location');
  const city = button.getAttribute('data-city');
  const contact = button.getAttribute('data-contact');

  document.getElementById('dermatologistId').value = id;
  document.getElementById('dermatologistDetails').value =
    `${name}, Expertise: ${expertise}, Clinic: ${clinic}, Contact: ${contact}, ${location}, ${city}`;
});
