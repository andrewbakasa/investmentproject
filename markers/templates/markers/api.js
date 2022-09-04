const copy = "© <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors";
const url = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
const osm = L.tileLayer(url, { attribution: copy });
const map = L.map("map", { layers: [osm] });
map.
locate()
  .on("locationfound", (e) => map.setView(e.latlng, 8))
  .on("locationerror", () => map.setView([0, 0], 5));

async function load_world_borders() {
    const world_border_url = `/api/world/?in_bbox=${map.getBounds().toBBoxString()}`
    const response = await fetch(world_border_url)
    const geojson = await response.json()
    return geojson
}
  
async function render_world_borders() {
    const world_borders = await load_world_borders();
    L.geoJSON(world_borders)
        .bindPopup((layer) => layer.feature.properties.name)
        .addTo(map);
}
  
  map.on("moveend", render_world_borders);



  async function render_world_borders() {
    const world_borders = await load_world_borders();
    L.geoJSON(world_borders)
        .bindPopup((layer) => layer.feature.properties.name)
        .addTo(map)
        .myTag = "myGeoJSON";
}

var removeMarkers = function() {
    map.eachLayer( function(layer) {

      if ( layer.myTag &&  layer.myTag === "myGeoJSON") {
        map.removeLayer(layer)
          }

        });

}

map.on("moveend", removeMarkers);

map.on("moveend", render_world_borders);




/* 
Since world borders GeoJSON data is requested by bounding box, you indeed have to clear previous features when loading new ones after map zoom or pan.

The simplest was to do that is to first create world borders layer at global level and then when new data is fetched, first clean it and than add new data.

Code could then look something like this:
 */
const bordersLayer = L.geoJSON(null)
  .bindPopup((layer) => layer.feature.properties.name)
  .addTo(map);

async function render_world_borders() {
  bordersLayer.clearLayers();
  const world_borders = await load_world_borders();
  bordersLayer.addData(world_borders);