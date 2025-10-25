function sendGetRequest(query, value) {
  // Construct the URL for your Django view
  // Replace '/my-django-view/' with your actual URL pattern
  // and 'selected_value' with the name of your GET parameter
  const url3 =
    window.location.origin + window.location.pathname + `?${query}=${value}`;

  window.location.href = url3; // Redirect the browser
}

document.addEventListener('DOMContentLoaded', function() {
  var map = L.map('map').setView([-12.100844, -77.044920], 16);
    
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
  }).addTo(map);


  const dataElement = document.getElementById('ruminants-list');
  const locations = JSON.parse(dataElement.textContent);
  // Example marker
  for (let i = 0; i < locations.length; i++) {
    console.log('hola'+i);
    L.marker([locations[i][0], locations[i][1]]).addTo(map);
  }
  L.marker([-12.100844, -77.044920]).addTo(map)
  .bindPopup('A pretty popup.')
    .openPopup()
});
