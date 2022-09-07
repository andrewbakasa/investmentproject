var cloudmade = L.tileLayer('http://{s}.tile.cloudmade.com/{key}/997/256/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: 'Map data &copy; 2011 OpenStreetMap contributors, Imagery &copy; 2011 CloudMade',
    key: 'BC9A493B41014CAABB98F0471D759707'
});

var map = L.map('map')
    .setView([50.5, 30.51], 15)
    .addLayer(cloudmade);

var markers = new L.FeatureGroup();

function getRandomLatLng(map) {
    var bounds = map.getBounds(),
        southWest = bounds.getSouthWest(),
        northEast = bounds.getNorthEast(),
        lngSpan = northEast.lng - southWest.lng,
        latSpan = northEast.lat - southWest.lat;

    return new L.LatLng(
    southWest.lat + latSpan * Math.random(),
    southWest.lng + lngSpan * Math.random());
}

function populate() {
    for (var i = 0; i < 10; i++) {
        var marker = L.marker(getRandomLatLng(map));
        marker.bindPopup("<p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Donec odio. Quisque volutpat mattis eros. Nullam malesuada erat ut turpis. Suspendisse urna nibh, viverra non, semper suscipit, posuere a, pede.</p><p>Donec nec justo eget felis facilisis fermentum. Aliquam porttitor mauris sit amet orci. Aenean dignissim pellentesque.</p>", {
            showOnMouseOver: true
        });
        markers.addLayer(marker);
    }
    return false;
}

map.addLayer(markers);

populate();
function removeAllMarkers(){
    map.removeLayer(markers);
}
document.querySelector('button').onclick=function(){removeAllMarkers()};
