// Handles the ticket form: on submit, validate the email
// against the same pattern the backend uses (schemas.py),
// build the ticket, and POST it to API_URL with fetch.
// Success shows the ticket ID and routing status in the
// result box below the form. An HTTP error or a failed
// connection shows an error message instead and leaves
// the form filled in, so the user can retry without
// retyping. The FastAPI endpoint replaces the httpbin
// test target in API_URL after the Friday sprint.

var form = document.getElementById('ticket-form');
var result = document.getElementById('ticket-result');
var emailInput = document.getElementById('email');
var subjectInput = document.getElementById('subject');
var bodyInput = document.getElementById('body');

// Today's test target: httpbin echoes back whatever JSON
// it receives, which proves the send worked end to end.
// Friday this points at the FastAPI endpoint instead.
var API_URL = 'https://httpbin.org/post';

// Same rule as InboundTicket.customer_email in schemas.py.
// Checked here in code because iOS Safari does not enforce
// the pattern attribute on the input itself.
var EMAIL_PATTERN = /^[\w.-]+@[\w.-]+\.\w+$/;

form.addEventListener('submit', async function (event) {
  event.preventDefault();

  var email = emailInput.value.trim();
  if (!EMAIL_PATTERN.test(email)) {
    result.textContent =
      'That email address is not in the correct format. ' +
      'Please use a full address, e.g. name@company.com.';
    emailInput.focus();
    return;
  }

  var ticket = {
    ticket_id: 'OF-' + Math.floor(100000 + Math.random() * 900000),
    customer_email: email,
    subject: subjectInput.value.trim(),
    body: bodyInput.value.trim(),
    created_at: new Date().toISOString()
  };

  result.textContent = 'Sending...';

  try {
    var response = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(ticket)
    });

    if (!response.ok) {
      result.textContent =
        'The server answered with an error (' + response.status + '). ' +
        'Your text is still in the form - try again.';
      return;
    }

    var stamp = new Date().toLocaleString('en-US', {
      dateStyle: 'medium',
      timeStyle: 'short'
    });

    result.textContent =
      'Ticket ID: ' + ticket.ticket_id + '\n' +
      'Submitted: ' + stamp + '\n' +
      'Status: Routed to the triage queue.';

    form.reset();
  } catch (error) {
    result.textContent =
      'Could not reach the server. ' +
      'Your text is still in the form - check your connection and try again.';
  }
});
