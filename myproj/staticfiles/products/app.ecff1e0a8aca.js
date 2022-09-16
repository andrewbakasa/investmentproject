

 var map = L.map('mapid').setView([51.505, -0.09], 13);

 var tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
     maxZoom: 19,
     attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
 }).addTo(map);

 const color = ["#fe4848", "#fe6c58", "#fe9068", "#feb478", "#fed686"];
 var user_loc_x = JSON.parse(document.getElementById('user-x-data').textContent);//--Long--
 var user_loc_y = JSON.parse(document.getElementById('user-y-data').textContent);//--Lat--
 var latest_user_loc_x=user_loc_x
 var latest_user_loc_y=user_loc_y 
 var accuracy ="Not Given"
 var var_redraw=true // at start
 function getToken(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
var csrftoken = getToken('csrftoken');
 
 //console.log ("val>>>",user_loc_x,user_loc_y,)
 var pA = new L.FeatureGroup();
 var pB = new L.FeatureGroup();
 var pointsA = [
     //           Lat                     Long
     [parseFloat(user_loc_y), parseFloat(user_loc_x), "view position"],
   ];

base_data_url_plus_coord = base_data_url.replace(/12345/, user_loc_x).replace(/6789/, user_loc_y);

 var dataurl = base_data_url_plus_coord;
 var map

 function removeAllMarkers(map,fgroup_markers){
     map.removeLayer(fgroup_markers);
     //clear contents
     removeallFeatures(fgroup_markers)
     //fgroup_markers = new L.FeatureGroup();
 }
 var mapMarkers = []
 window.addEventListener("map:init", function (event) {
   //console.log('in init:')
   map = event.detail.map;
   //console.log("url")
   //console.log(dataurl)

   
   addClick()
   // Download GeoJSON data with Ajax
   fetch(dataurl
    // , 
    //   {
    //     method: 'GET',
    //     headers: {
    //       'Content-Type':'application/json',
    //       'X-CSRFToken':csrftoken,
    //     },
    //     body: JSON.stringify({'productId': 1, 'action': 1})
    //   }
     ).then(function(resp) {
       //console.log('RESPONSONSE 111.:', resp)
       return resp.json();
     })
     .then(function(data) {
       //console.log('fetching data:', data)
       //clear Product Data
       $('.apartments').html("")
       L.geoJson(data, {
         pointToLayer: function(feature, latlng) {
           const smallIcon = L.divIcon({
             className: "marker",
             html: svgTemplateColor('#2b92eb'),//color[5]),
             iconSize: [40, 40],
             iconAnchor: [12, 24],
             popupAnchor: [7, -16],
           });
            // Add marker to this.mapMarker for future reference
            mapMarkers.push(L.marker(latlng, {icon: smallIcon}));
          
           return L.marker(latlng, {icon: smallIcon});
         },
         onEachFeature: function onEachFeature(feature, layer) {
           var props = feature.properties;
           //console.log('Prop:', props)
          
           var content 
           // append data
           a_html=append_html(props)                 
           $(a_html).bind("mouseover",function(){
                map.flyTo([layer.feature.geometry.coordinates[1],layer.feature.geometry.coordinates[0]],9)
           }).appendTo($('.apartments'));
           //-----------------------------
           if (props.image) {
             content = `<img width="100" object-fit: cover ; src="${props.image}" </br><p>${props.name} &nbsp;<i class="fas fa-map-marker-alt"></i>${nFormatterdist(props.distance,1)} </br> $${nFormatter(props.price,2)}</p>`;
          
           } else {
             content = `<img width="100"  object-fit: cover ;src=""/><h3>${props.name}</h3><p>${props.name}&nbsp;<i class="fas fa-map-marker-alt"></i>${nFormatterdist(props.distance,1)}</br> $${nFormatter(props.price,2)}</p>`;
          
           }
           //content.setStyle({fillColor :'blue'})
          // let tooltip = L.tooltip({
          //   permanent:true
          // }).setContent(props.price)
          layer.bindPopup(content)//.bindTooltip(tooltip);
           pB.addLayer(layer);

       }})//.addTo(map);
       // origin::::::
       map.addLayer(pB);
       set_map(map)
       var element = document.getElementById('add-button-id');
       //trigger 
       element.click()
     });

 });


function numberWithCommas(x) {
var parts = x.toString().split(".");
parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
return parts.join(".");
}
// Pass the layerGroup to the function
function removeallFeatures(layerGroup) {
// Use getLayers to get the array
var layerArr = layerGroup.getLayers();
// Use eachLayer to iterate the layerGroup
layerGroup.eachLayer((layer) => {
   layerGroup.removeLayer(layer);
});
}

function svgTemplateColor(color){
const svgTemplate = `
 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" class="marker">
   <path fill-opacity=".25" d="M16 32s1.427-9.585 3.761-12.025c4.595-4.805 8.685-.99 8.685-.99s4.044 3.964-.526 8.743C25.514 30.245 16 32 16 32z"/>
   <path stroke="#fff" fill="${color}" d="M15.938 32S6 17.938 6 11.938C6 .125 15.938 0 15.938 0S26 .125 26 11.875C26 18.062 15.938 32 15.938 32zM16 6a4 4 0 100 8 4 4 0 000-8z"/>
 </svg>`
return svgTemplate
}
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
document.addEventListener("DOMContentLoaded", function(event) {

    //formElem =document.getElementById('form')
    btn =document.getElementById('btn')
    btn.addEventListener("click", myScript);
   
    //console.log('...', formElem)
    
 
  //trigger
  $('#btn').click()
 
}) 
function set_map(map){
    
    map.setView([parseFloat(user_loc_y), parseFloat(user_loc_x)], 5);
     
    const allMarkers = new L.FeatureGroup();
    // adding markers to the layer pointsA
    for (let i = 0; i < pointsA.length; i++) {
      
      marker_label= `Standing postion <br>${pointsA[i][2]}`
      marker = L.marker([pointsA[i][0], pointsA[i][1]], {
                    icon: colorMarker(color[index_a]),
                }).bindPopup(marker_label);

      pA.addLayer(marker);
    }


    // object with layers
    const overlayMaps = {
        "View Point": pA,
        //"point B": pB,
      };
    
    
    // centering a group of markers
    map.on("layeradd layerremove", function () {
      var  layers_count=0
      // Create new empty bounds
      let bounds = new L.LatLngBounds();
      // Iterate the map's layers
      map.eachLayer(function (layer) {
        // Check if layer is a featuregroup
        if (layer instanceof L.FeatureGroup) {
          // Extend bounds with group's bounds
          bounds.extend(layer.getBounds());
          //layers_count +=1
          //console.log(" 1. lay: prop>>>", layer.getLayers().length)
          //layer.getLayers()
          if (layer.getLayers().length>0){
            
            layers_count +=1
            //console.log("Total>>>", layer.getLayers().length)
          }
          if (layer.getLayers().length>1){
            // add other so that in breach the pass mark of 1
            layers_count +=1
          } 
        }
      });
    
      // Check if bounds are valid (could be empty)
      if (bounds.isValid() && layers_count>1) {
        // Valid, fit bounds
        //console.log('Valid bounds', layers_count)
        map.flyToBounds(bounds);
      } else {
        //console.log('No valid bounds',layers_count)
        // Invalid, fit world
        map.fitWorld();
      }
    });
   
    
    new L.Control.CustomButtons(null, overlayMaps, { collapsed: false }).addTo(map);
  }
  
  function get_bounds_and_resize_MapView(redraw=true){
    var layers_count =0
      // Create new empty bounds
      let bounds = new L.LatLngBounds();
      // Iterate the map's layers
      map.eachLayer(function (layer) {
        // Check if layer is a featuregroup
        if (layer instanceof L.FeatureGroup) {
          // Extend bounds with group's bounds
          bounds.extend(layer.getBounds());
          //console.log(" lay: lenght and layer_count>>>", layer.getLayers().length, layers_count)
          if (layer.getLayers().length>0){
            
            layers_count +=1
            //console.log("Total>>>", layer.getLayers().length)
          }
          if (layer.getLayers().length>1){
          // add other so that in breach the pass mark of 1
          layers_count +=1
        } 
        }
      });
      //console.log("markers count 333 :", layers_count)
      // Check if bounds are valid (could be empty)
      if (bounds.isValid() && layers_count > 1) {
        // Valid, fit bounds
        //console.log('Valid bounds')
        if (redraw)
          map.flyToBounds(bounds);
      } else {
        //console.log('No valid bounds')
        // Invalid, fit world
        map.fitWorld();
      }
  }

  $('body').on('click', '.product-tag', function (e) {
    e.preventDefault();
    var tr_id = $(this).attr('data-item-id')
   /* row = $('#'+ tr_id.trim()); */ 
    //console.log("found",tr_id, e.target)
  })
 


function append_html(val){
        var prod_url = ''
        //console.log('ITERATION', val)
        if (val.image !== null) {
            prod_url =`<img src="${val.image}" class="img-fluid product-tag" data-item-id="${val.pid}}">`
        }else {
            prod_url=` <img  src="${default_img}" class="img-fluid product-tag" data-item-id="${val.pid}}">`
        }
        
    
        a_html =`<div id="${val.pid}" class="col-lg-4 annotation">                   
                    ${prod_url}
                    <h5>
                      <a data-toggle="tooltip" data-placement="bottom" 
                          title='View Prorduct Details' 
                           href="/e/p/d/${val.pid}/">${val.name}
                       </a> &nbsp;<i class="fas fa-map-marker-alt"></i>${nFormatterdist(val.distance,1)}
                    </h5>
                    <p>$${nFormatter(val.price,2)}</p>
                </div>`
                  
  return a_html
}
function nFormatterdist(num, digits) {
  //digits=1
  const lookup = [
      { value: 1, symbol: "m" },
      { value: 1e3, symbol: "km" },
      // { value: 1e6, symbol: ",000 km" },
      // { value: 1e9, symbol: "Gm" },
      // { value: 1e12, symbol: "Tm" },
      // { value: 1e15, symbol: "Pm" },
      // { value: 1e18, symbol: "Em" }
  ];
  const rx = /\.0+$|(\.[0-9]*[1-9])0+$/;
  var item = lookup.slice().reverse().find(function(item) {
      return num >= item.value;
  });
  prenum= item ? (num / item.value).toFixed(digits).replace(rx, "$1") + item.symbol : "0";
  return numberWithCommas(prenum)
}

function nFormatter(num, digits) {
  //digits=1
  const lookup = [
      { value: 1, symbol: "" },
      { value: 1e3, symbol: "k" },
      { value: 1e6, symbol: "M" },
      { value: 1e9, symbol: "G" },
      { value: 1e12, symbol: "T" },
      { value: 1e15, symbol: "P" },
      { value: 1e18, symbol: "E" }
  ];
  const rx = /\.0+$|(\.[0-9]*[1-9])0+$/;
  var item = lookup.slice().reverse().find(function(item) {
      return num >= item.value;
  });
  return item ? (num / item.value).toFixed(digits).replace(rx, "$1") + item.symbol : "0";
}

    if (!navigator.geolocation){
      console.log ("Your browser doesn't support geolocation feature!")
      $('#total_projects_searched').text("Your browser doesn't support geolocation feature!")
    }else {
      const options = {
        enableHighAccuracy: true,
        timeout: 5000,
        maximumAge: 0
      };
      setInterval(()=> {
        navigator.geolocation.getCurrentPosition(getPosition, error, options)
        $('#total_projects_searched').html("<b>Your Location </b>Lat: <i style='background-color:yellow'>" + user_loc_x + "</i> Long: <i style='background-color:yellow'>" + user_loc_y + "</i> Accuracy: <i style='background-color:greenyellow'>"+ nFormatterdist(accuracy,1) +"</i>")
      }, 15000)
    }
   


function error(err) {
  console.warn(`ERROR(${err.code}): ${err.message}`);
}
var marker, circle
const curr_pos_smallIcon = L.divIcon({
  className: "marker",
  html: svgTemplateColor('#fe6c58'),//color[5]),
  iconSize: [40, 40],
  iconAnchor: [12, 24],
  popupAnchor: [7, -16],
});

function getPosition(position){
  //console.log(position)
  var lat= position.coords.latitude
  var lang =position.coords.longitude
  accuracy = position.coords.accuracy
  
  //------change user position------------------------------
  user_loc_x = lang
  user_loc_y = lat
  pointsA = [
    //           Lat                     Long
    [parseFloat(user_loc_y), parseFloat(user_loc_x), "view position"],
  ];
  //--------------------------------------------------


  
  //console.log('Cart: ', cart)
  document.cookie = 'userlocation=' + JSON.stringify([lat,lang]) + ";domain=;path=/"
  
  console.log('Your coordinate is Lat ' + lat + " Long: " + lang + " Accuracy: " + accuracy)
  
  //hit database and refress
  //calcultate if user has moved significantly from last position
  if (get_transition_metre(5)){// at every 5 metres refresh
    myScript(var_redraw)
    var_redraw=false
  }
  
}
function myScript(redraw=true){
 
  // keep last position
  latest_user_loc_x = user_loc_x 
  latest_user_loc_y = user_loc_y
  //remove previous markers of recent search
  removeAllMarkers(map,pB)
  removeAllMarkers(map,pA)
  pB = new L.FeatureGroup();
  var search_val = document.getElementById('start').value//.toLowerCase();
  search_val=search_val.replace(/[^a-zA-Z0-9]/g,"")

  //console.log('search ' , search_val)
  if (search_val.length>0){            
    dataurl = slug_data_url.replace(/12345/, search_val.toString()).replace(/68/, user_loc_x).replace(/89/, user_loc_y); 
    
  }else {
    //all products
    dataurl = base_data_url.replace(/12345/, user_loc_x).replace(/6789/, user_loc_y);;

  }

   
  // Download GeoJSON data with Ajax
    fetch(dataurl
      // , 
      // {
      //   method: 'GET',
      //   headers: {
      //     'Content-Type':'application/json',
      //     'X-CSRFToken':csrftoken,
      //   },
      //   body: JSON.stringify({'productId': 1, 'action': 1})
      // }
      ).then(function(resp) {
        //console.log('RESPONSONSE 111.:', resp)
        return resp.json();
      })
      .then(function(data) {
        //console.log('fetching data:', data)
        //clear Product Data
        $('.apartments').html("")
        L.geoJson(data, {
          pointToLayer: function(feature, latlng) {
            const smallIcon = L.divIcon({
              className: "marker",
              html: svgTemplateColor('#2b92eb'),//color[5]),
              iconSize: [40, 40],
              iconAnchor: [12, 24],
              popupAnchor: [7, -16],
            });
            
            return L.marker(latlng, {icon: smallIcon});
          },
          onEachFeature: function onEachFeature(feature, layer) {
            var props = feature.properties;
            //console.log('Prop:', props)
           
            var content 
            //-- append data------
            a_html=append_html(props)                 
           $(a_html).bind("mouseover",function(){                    
              map.flyTo([layer.feature.geometry.coordinates[1],layer.feature.geometry.coordinates[0]],9)
           }).appendTo($('.apartments'));
            //-------------------
            if (props.image) {
              content = `<img width="100" object-fit: cover ; src="${props.image}" </br><p>${props.name} &nbsp;<i class="fas fa-map-marker-alt"></i>${nFormatterdist(props.distance,1)}</br> $${nFormatter(props.price,2)} </p>`;
          
            } else {
              content = `<img width="100"  object-fit: cover ;src=""/><h3>${props.name}</h3><p>${props.name}&nbsp;<i class="fas fa-map-marker-alt"></i>${nFormatterdist(props.distance,1)}</br> $${nFormatter(props.price,2)}</p>`;
          
            }
            //content.setStyle({fillColor :'blue'})
            //console.log('This LAy>>>>>>>>>>>>>>', layer.feature.geometry.coordinates)
            // let tooltip = L.tooltip({
            //   permanent:true
            // }).setContent(props.price)
            layer.bindPopup(content)//.bindTooltip(tooltip); 
            pB.addLayer(layer);
        }})//.addTo(map);
      // origin::::::
      map.addLayer(pB);
      //set_map(map)
      //var element = document.getElementById('add-button-id');
      //trigger 
      //element.click()
      addStartPoint()
      get_bounds_and_resize_MapView(redraw)
     
    });

};
function addStartPoint(){
  removeAllMarkers(map,pA)
  //pA = new L.FeatureGroup();
  //const allMarkers = new L.FeatureGroup();
  // adding markers to the layer pointsA
  for (let i = 0; i < pointsA.length; i++) {
    
    marker_label= `Standing postion <br>${pointsA[i][2]}`
    marker = L.marker([pointsA[i][0], pointsA[i][1]], {
                  icon: colorMarker(color[index_a]),
              }).bindPopup(marker_label);

    pA.addLayer(marker);
  }
  map.addLayer(pA);
}

function get_transition_metre(bound_m){
 

  let user_latlng1 = L.latLng(user_loc_x, user_loc_y);
  let latest_latlng2 = L.latLng(latest_user_loc_x, latest_user_loc_y);

  let distance = user_latlng1.distanceTo(latest_latlng2)//    / 1000
  
  console.log('Change in distance moved: ', distance , ' map redraws if distance is at least ',bound_m , " metres");
  if (distance > bound_m){
    return true
  }
  return false
}









