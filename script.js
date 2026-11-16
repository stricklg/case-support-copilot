// Handles the ticket form: on submit, validate the email
// against the same pattern the backend uses (schemas.py),
// then assign a ticket ID, stamp the date/time, and show
// both in the result box below the form. The real
// triage-queue call lands with the FastAPI endpoint
// (Friday's sprint); today this confirms the routing
// on the page.
var form = document.getElementById('ticket-form');
var result = document.getElementById('ticket-result');
var emailInput = document.getElementById('email');

// Same rule as InboundTicket.customer_email in schemas.py.
// Checked here in code because iOS Safari does not enforce
// the pattern attribute on the input itself.
var EMAIL_PATTERN = /^[\w.-]+@[\w.-]+\.\w+$/;

form.addEventListener('submit', function (event) {
  event.preventDefault();

  var email = emailInput.value.trim();
  if (!EMAIL_PATTERN.test(email)) {
    result.textContent =
      'That email address is not in the correct format. ' +
      'Please use a full address, e.g. name@company.com.';
    emailInput.focus();
    return;
  }

  var ticketId = 'OF-' + Math.floor(100000 + Math.random() * 900000);
  var stamp = new Date().toLocaleString('en-US', {
    dateStyle: 'medium',
    timeStyle: 'short'
  });

  result.textContent =
    'Ticket ID: ' + ticketId + '\n' +
    'Submitted: ' + stamp + '\n' +
    'Status: Routed to the triage queue.';

  form.reset();
});
