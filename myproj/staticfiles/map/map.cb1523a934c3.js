

//var l = JSON.parse("{{json_user_location}}")
const user_loc_x = JSON.parse(document.getElementById('user-x-data').textContent);
const user_loc_y = JSON.parse(document.getElementById('user-y-data').textContent);
// coordinate array with popup text
console.log ("val>>>",user_loc_x,user_loc_y,)

const pointsA = [
    [parseFloat(user_loc_x), parseFloat(user_loc_y), "view position"],
  ];
const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
const map = L.map('map')
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', 
  { attribution: 
    attribution }).addTo(map);

const markers = JSON.parse(document.getElementById('markers-data').textContent);
let feature = L.geoJSON(markers).bindPopup(function (layer) { return layer.feature.properties.name;
 }).addTo(map);

map.fitBounds(feature.getBounds(), { padding: [100, 100] });



// obtaining coordinates after clicking on the map
map.on("click", function (e) {
    const markerPlace = document.querySelector(".marker-position");
    markerPlace.textContent = e.latlng;
  });
  


// Extended `LayerGroup` that makes it easy
// to do the same for all layers of its members
const pA = new L.FeatureGroup();
const allMarkers = new L.FeatureGroup();

// color table
const color = ["#fe4848", "#fe6c58", "#fe9068", "#feb478", "#fed686"];
// the function creates colorful svg
function colorMarker(color) {
    const svgTemplate = `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" class="marker">
        <path fill-opacity=".25" d="M16 32s1.427-9.585 3.761-12.025c4.595-4.805 8.685-.99 8.685-.99s4.044 3.964-.526 8.743C25.514 30.245 16 32 16 32z"/>
        <path stroke="#fff" fill="${color}" d="M15.938 32S6 17.938 6 11.938C6 .125 15.938 0 15.938 0S26 .125 26 11.875C26 18.062 15.938 32 15.938 32zM16 6a4 4 0 100 8 4 4 0 000-8z"/>
      </svg>`;
  
    const icon = L.divIcon({
      className: "marker",
      html: svgTemplate,
      iconSize: [40, 40],
      iconAnchor: [12, 24],
      popupAnchor: [7, -16],
    });
  
    return icon;
  }
index_a=1
// adding markers to the layer pointsA
for (let i = 0; i < pointsA.length; i++) {
  marker_label= `color: #${color[index_a]}<br>${pointsA[i][2]}`
  marker = L.marker([pointsA[i][0], pointsA[i][1]], {
                icon: colorMarker(color[index_a]),
            }).bindPopup(marker_label);

  pA.addLayer(marker);
}


// object with layers
const overlayMaps = {
    "View Point": pA,
    // "point B": pB,
  };
  
  // centering a group of markers
  map.on("layeradd layerremove", function () {
    // Create new empty bounds
    let bounds = new L.LatLngBounds();
    // Iterate the map's layers
    map.eachLayer(function (layer) {
      // Check if layer is a featuregroup
      if (layer instanceof L.FeatureGroup) {
        // Extend bounds with group's bounds
        bounds.extend(layer.getBounds());
      }
    });
  
    // Check if bounds are valid (could be empty)
    if (bounds.isValid()) {
      // Valid, fit bounds
      map.flyToBounds(bounds);
    } else {
      // Invalid, fit world
      // map.fitWorld();
    }
  });
  
  L.Control.CustomButtons = L.Control.Layers.extend({
    onAdd: function () {
      this._initLayout();
      this._addMarker();
      this._removeMarker();
      this._update();
      return this._container;
    },
    _addMarker: function () {
      this.createButton("add", "add-button");
    },
    _removeMarker: function () {
      this.createButton("remove", "remove-button");
    },
    createButton: function (type, className) {
      const elements = this._container.getElementsByClassName(
        "leaflet-control-layers-list"
      );
      const button = L.DomUtil.create(
        "button",
        `btn-markers ${className}`,
        elements[0]
      );
      button.textContent = `${type} markers`;
  
      L.DomEvent.on(button, "click", function (e) {
        const checkbox = document.querySelectorAll(
          ".leaflet-control-layers-overlays input[type=checkbox]"
        );
  
        // Remove/add all layer from map when click on button
        [].slice.call(checkbox).map((el) => {
          el.checked = type === "add" ? false : true;
          el.click();
        });
      });
    },
  });
  
  new L.Control.CustomButtons(null, overlayMaps, { collapsed: false }).addTo(map);
