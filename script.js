// Handles the ticket form: on submit, validate the email
// against the same pattern the backend uses (schemas.py),
// build the ticket, and POST it to API_URL with fetch.
// Success shows the ticket ID and the triage category
// and priority the API returned, in the result box below
// the form. An HTTP error or a failed connection shows
// an error message instead and leaves the form filled
// in, so the user can retry without retyping.

var form = document.getElementById('ticket-form');
var result = document.getElementById('ticket-result');
var emailInput = document.getElementById('email');
var subjectInput = document.getElementById('subject');
var bodyInput = document.getElementById('body');

// The capstone's FastAPI endpoint (uvicorn on this
// machine, port 8000). It receives the ticket, runs it
// through the triage pipeline, and returns the result.
var API_URL = 'http://localhost:8000/tickets';

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

    var data = null;
    try {
      data = await response.json();
    } catch (parseError) {
      data = null;
    }

    var stamp = new Date().toLocaleString('en-US', {
      dateStyle: 'medium',
      timeStyle: 'short'
    });

    var statusLine = 'Status: Routed to the triage queue.';
    if (data && data.category) {
      statusLine =
        'Category: ' + data.category + '\n' +
        'Priority: ' + data.priority;
    }

    result.textContent =
      'Ticket ID: ' + ticket.ticket_id + '\n' +
      'Submitted: ' + stamp + '\n' +
      statusLine;

    form.reset();
  } catch (error) {
    result.textContent =
      'Could not reach the server. ' +
      'Your text is still in the form - check your connection and try again.';
  }
});
