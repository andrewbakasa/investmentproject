var shopAddress = document.querySelector("#address")
var addresses = document.querySelector('#addresses')
var address= document.querySelector("#id_address")
var lat= document.querySelector("#id_lat")
var lng= document.querySelector("#id_lng")
var standard_zoom =15
//var mapMarkers
function showAddresses(){
    addresses.innerHTML = ""
    if (addressData.length  > 0 ){
        //console.log(addressData)
            addressData.forEach(address => {
                addressName = address.display_name.replace(/'/g, " ");
                addresses.innerHTML += `<div class="results" onclick ="selectAddress(${address.lat},
                    ${address.lon}, &apos;${addressName}&apos;)"> ${address.display_name}</div>`
                //console.log(address)    

            });
    }
}
function selectAddress(x,y,adr){
    //console.log('Here...' ,x,y,adr)
    address.value =adr
    lat.value=x
    lng.value=y
    map.flyTo([x,y],15)
    marker.closePopup()
    marker.setLatLng([x,y])

}


function findAddresses(){
    url ="https://nominatim.openstreetmap.org/search?format=json&limit=3&q=" + shopAddress.value
    fetch(url)
    .then(response=> response.json())
    .then(data=> addressData=data)
    .then(showAddress =>showAddresses())
}

var map = L.map('mapid').setView([51.505, -0.09], 13);

var tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);
var marker = L.marker([51.505, -0.09]).addTo(map)


map.on('click', function(e) {
    //console.log(e.latlng.lat,e.latlng.lng);
    let click_zoom =standard_zoom
    x=e.latlng.lat
    y=e.latlng.lng
    lat.value=x
    lng.value=y
    //if current zoom is gether that standard zoom
    if (map.getZoom() > standard_zoom){
        click_zoom = map.getZoom()
    }
        
    map.flyTo([x,y],click_zoom)
    marker.closePopup()
    marker.setLatLng([x,y])
  
  });