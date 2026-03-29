var shop_loc_x = JSON.parse(document.getElementById('user-x-data').textContent);//--Long--
var shop_loc_y = JSON.parse(document.getElementById('user-y-data').textContent);//--Lat-
console.log("x:y coord:", shop_loc_x,shop_loc_y)
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
    lng.value=x
    lat.value=y
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

var marker 
if (!(shop_loc_y==null) && !(shop_loc_y ==null)){//
  marker = L.marker([51.505, -0.09]).addTo(map)

}else {
  marker = L.marker([shop_loc_x, shop_loc_y]).addTo(map)
}


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

  if (!(shop_loc_y==null) && !(shop_loc_y ==null)){//
    //Update the address
    map.setView([parseFloat(shop_loc_y), parseFloat(shop_loc_x)], 13);
    marker.setLatLng([shop_loc_y,shop_loc_x])
  }else {  
        if (!navigator.geolocation){
          console.log ("Your browser doesn't support geolocation feature!")
          $('#total_projects_searched').text("Your browser doesn't support geolocation feature!")
        }else {
   
              var options
              browserChrome = navigator.userAgent.includes("Chrome")
              if (browserChrome) //set this var looking for Chrome un user-agent header
                  options={enableHighAccuracy: true, maximumAge: 75000, timeout: 80000};
              else
                  options={enableHighAccuracy: true, maximumAge:Infinity, timeout:80000};
              
            
                  var watchID = navigator.geolocation.watchPosition(getPosition, showError, options );
                  var timeout = setTimeout( ()=> { 
                      navigator.geolocation.clearWatch(watchID); 
                      
                  }, 15000 );
            
        }   
  }


  function getPosition(position){
    //console.log(position)
    var lat= position.coords.latitude
    var lang =position.coords.longitude
    accuracy = position.coords.accuracy
  
  

    map.setView([parseFloat(lat), parseFloat(lang)], 13);
   
  
    console.log('Watching Position: Your coordinate is Lat ' + lat + " Long: " + lang + " Accuracy: " + accuracy)
    
    
  } 
  function showError(error) {
    switch(error.code) {
      case error.PERMISSION_DENIED:
        $('#total_projects_searched').html("User denied the request for Geolocation.")
        break;
      case error.POSITION_UNAVAILABLE:
        $('#total_projects_searched').html("Location information is unavailable.")
        break;
      case error.TIMEOUT:
        $('#total_projects_searched').html("The request to get user location timed out.")
        break;
      case error.UNKNOWN_ERROR:
        $('#total_projects_searched').html( "An unknown error occurred.")
        break;
    }
  }   