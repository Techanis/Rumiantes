function sendGetRequest(query, value) {
  // Construct the URL for your Django view
  // Replace '/my-django-view/' with your actual URL pattern
  // and 'selected_value' with the name of your GET parameter
  const url3 =
    window.location.origin + window.location.pathname + `?${query}=${value}`;

  window.location.href = url3; // Redirect the browser
}
