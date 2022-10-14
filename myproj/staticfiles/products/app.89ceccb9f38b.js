
 var user_loc_x = JSON.parse(document.getElementById('user-x-data').textContent);//--Long--
 var user_loc_y = JSON.parse(document.getElementById('user-y-data').textContent);//--Lat--
 var current_page_no =1 //default
 //var rowpagedata  = JSON.parse(document.getElementById('pagedata-input').textContent);//--Lat--
 
 var map = L.map('mapid').setView([user_loc_x, user_loc_y], 13);
 var bounds = L.latLngBounds() // Instantiate LatLngBounds object
 var color = ["#fe4848", "#fe6c58", "#fe9068", "#feb478", "#fed686"];
 
 //console.log('page data>>>>>', pagedata);
 var t1 = null
 var dif_seconds =0
 var counter=0
 let id_found =[]
 index_a=1
 var marker, circle
 set_map(map)
 
 var tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
     maxZoom: 19,
     attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
 }).addTo(map);

 
 var latest_user_loc_x=user_loc_x
 var latest_user_loc_y=user_loc_y 
 var accuracy ="Not Given"
 var var_fly_bounds=true // at start
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
 //var pA = new L.FeatureGroup();
 var pB = new L.FeatureGroup();
//  var pointsA = [
//      //           Long                     Lat
//      [parseFloat(user_loc_x), parseFloat(user_loc_y), "view position"],
//    ];

base_data_url_plus_coord = base_data_url.replace(/12345/, user_loc_x)
                          .replace(/6789/, user_loc_y)
                          .replace(/444444/, 1) ;;

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
  while (id_found.length > 0) {
    id_found.pop();
  } // Fastest
   id_found.push('marker')
   //insert_initial()
   //addClick()
   // Download GeoJSON data with Ajax
   fetch(dataurl
     ).then(function(resp) {
       return resp.json();
     })
     .then(function(data) {
       //console.log('*****  MyScript: data features...', data.features)
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
            mapMarkers.push(L.marker(latlng, {icon: smallIcon},{myCustomId: 0}));
          
           return L.marker(latlng, {icon: smallIcon},{myCustomId: 0});
         },
         onEachFeature: function onEachFeature(feature, layer) {
           var props = feature.properties;
           //console.log('Prop:', props)
          
           var content 
           // append data
               
           let lat_lng = [layer.feature.geometry.coordinates[1],layer.feature.geometry.coordinates[0]]
           bounds.extend(lat_lng)      // Extend LatLngBounds with coordinates 
           a_html=append_html(props)
           $(a_html).bind("mouseover",function(){
                map.flyTo([layer.feature.geometry.coordinates[1],layer.feature.geometry.coordinates[0]],12)
           }).appendTo($('.apartments'));
           //-----------------------------
           anchor_tag =`<a data-toggle="tooltip" data-placement="bottom" title='View Prorduct Details' href="/e/p/d/${props.pid}/">${props.name}</a>`
        
           if (props.image) {
             content = `<img  style="width:100%;height:100px; object-fit: cover;" src="${props.image}"/></br><p><i style='color:blue'>Shopname</i>: ${props.shopname}</br><i style='color:blue'>Prod</i>: ${anchor_tag} &nbsp;<i class="fas fa-map-marker-alt"></i>${nFormatterdist(props.distance,1)}&nbsp; $${nFormatter(props.price,2)}</p>`;
          
           } else {
             content = `<img                                                       src=""             /></br><p><i style='color:blue'>Shopname</i>: ${props.shopname}</br><i style='color:blue'>Prod</i>: ${anchor_tag} &nbsp;<i class="fas fa-map-marker-alt"></i>${nFormatterdist(props.distance,1)} &nbsp;  $${nFormatter(props.price,2)}</p>`;
          
           }
          
          layer.bindPopup(content)
          layer.bindTooltip(
            '<small>$' + props.price +"</small>",
              {
                direction: 'right',
                permanent: true,
                sticky: true,
                offset: [10, 0],
                opacity: 0.65,
                className: 'leaflet-tooltip-own' 
              });

          layer._id = props.pid
        
          let tag_found=false
          pB.eachLayer(function(ll){
               
            if (ll._id == props.pid){
              //console.log('test_lay::::' , ll);
              tag_found=true
              if (!(id_found.includes(props.pid))){
                id_found.push(props.pid)
              }
            }
          })
          if (!tag_found){
            pB.addLayer(layer);
            map.addLayer(layer);
            if (!(id_found.includes(props.pid))){
              id_found.push(props.pid)
            }
          }

         
         
       }})//.addTo(map);
       // origin::::::
       pB.eachLayer(function(ll){
        if (!(id_found.includes(ll._id))){
          // new product search drop other products
          //console.log('removed',ll._id)
          map.removeLayer(ll)
        }else{
          // console.log('not removed',ll._id) 
        }
      })
    
     
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

document.addEventListener("DOMContentLoaded", function(event) {

 
  //trigger
  $('#btn').click()
 
}) 


function set_map(map){
    marker_label= `Standing position <br>View`
    marker = L.marker([user_loc_y, user_loc_x], {
                  icon: colorMarker(color[index_a]),
              }).bindPopup(marker_label);

    marker._id='marker'
    map.addLayer(marker);
    id_found.push('marker')

    
    circle = L.circle([user_loc_y, user_loc_x], 500, {
      color: 'red',
      fillColor: '#f03',
      fillOpacity: 0.5
    }).addTo(map).bindPopup("Accuracy.");

   
    
    circle._id='circle_marker'
    map.addLayer(circle);
    id_found.push('circle_marker')
   
}
  
  function get_bounds_and_resize_MapView(){
    
      if (bounds.isValid() ) {//&& layers_count > 0
        //console.log('1. Valid bounds',var_fly_bounds)
        if (var_fly_bounds == true){
          map.flyToBounds(bounds);
        }else{
          // removed fly to bound not user friendly: should keep map stable
          /* This is giving a problem 19 09 2022 @ 0741hrs */
          //map.setView([parseFloat(user_loc_x), parseFloat(user_loc_y)], map.getZoom());
        }         
      } else {
      
        // Invalid, fit world
        map.fitWorld();
      }

      if (dif_seconds > 30)// myScript run on promise// deactivate here
        var_fly_bounds=false//
         //update time        
        t1 = Date.now();
  }

  $('body').on('click', '.product-tag', function (e) {
    e.preventDefault();
    var tr_id = $(this).attr('data-item-id')
   
  })

  $('body').on('click', '#btn', function (e) {
    e.preventDefault();
    var_fly_bounds=true
    //reset to first page
    current_page_no=1   
    myScript()
  })
 
  $('body').on('keyup', '#start', function (e) {
    e.preventDefault();
    if(e.keyCode == 13)  // the enter key code
     {
        var_fly_bounds=true
        //reset to first page
        current_page_no=1   
        myScript()
       return false;  
     }
    
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
      /* const options = {
        enableHighAccuracy: true,
        timeout: 5000,
        maximumAge: 0
      }; */
      var options
      browserChrome = navigator.userAgent.includes("Chrome")
      //console.log(navigator.userAgent)
      //console.log(browserChrome)
      if (browserChrome) //set this var looking for Chrome un user-agent header
          options={enableHighAccuracy: true, maximumAge: 75000, timeout: 80000};
      else
          options={enableHighAccuracy: true, maximumAge:Infinity, timeout:80000};
      
       
        //const options = { enableHighAccuracy: true, maximumAge: Infinity, timeout: 50000 };
     
        var watchID = navigator.geolocation.watchPosition(getPosition, showError, options );
        var timeout = setTimeout( ()=> { 
            //navigator.geolocation.clearWatch(watchID); 
            $('#total_projects_searched').html("<b>Your Location </b>Long: <i style='background-color:yellow'>" + user_loc_x + "</i> Lat: <i style='background-color:yellow'>" + user_loc_y + "</i> Accuracy: <i style='background-color:greenyellow'>"+ nFormatterdist(accuracy,1) +"</i>" + " Time-diff: <i style='background-color:lightgreen'>" + dif_seconds.toFixed(0) +"s</i>")
        }, 15000 );
     
      // setInterval(()=> {
      //   navigator.geolocation.getCurrentPosition(getPosition, showError, options)
      //   $('#total_projects_searched').html("<b>Your Location </b>Long: <i style='background-color:yellow'>" + user_loc_x + "</i> Lat: <i style='background-color:yellow'>" + user_loc_y + "</i> Accuracy: <i style='background-color:greenyellow'>"+ nFormatterdist(accuracy,1) +"</i>")
      // }, 15000)//every 15seconds
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

  
  var newLatLng = new L.LatLng(lat, lang);
  marker.setLatLng(newLatLng);

  circle.setLatLng(newLatLng);
  //update radius
  circle.setRadius(accuracy)
  circle.setPopupContent('Accuracy :' + nFormatterdist(accuracy,1) )

  var today = new Date()
  //------change user position------------------------------
  user_loc_x = lang
  user_loc_y = lat
  pointsA = [
    //           Lat                     Long
    [parseFloat(lat), parseFloat(lang), "view position @ timestamp:" + today ],
  ];
  //--------------------------------------------------


  console.log('Watching Position: Your coordinate is Lat ' + lat + " Long: " + lang + " Accuracy: " + accuracy)
  
  //hit database and refress
  //calcultate if user has moved significantly from last position
  if (get_transition_metre(5)){// at every 5 metres change redrw map

    if (t1 !== null){
        let t2 = Date.now();
        //get seconds
        dif_seconds = ( t2 - t1) / 1000;
        console.log('Watching Position: seconds from last update', dif_seconds)
        
      
        if (dif_seconds > 15)// only go here id 30 seconds from last myScript run has passed
           //run promise
            myScript()
            //var_fly_bounds=false//
            //update time        
            //t1 = Date.now();

    }else{// for the first time.....
        //get durrent time  
        //console.log('.....here first time')      
        t1 = Date.now();
        //init running
        myScript()
        //var_fly_bounds=false//
    }
  }
  
}
function insert_initial(){
  return 
  console.log('::::::NEWNEW 1111', id_found)
  map.eachLayer(function(ll){
    if (!(id_found.includes(ll._id))){
      id_found.push(ll._id)
    }
  })
  console.log('::::::AFTER', id_found)
}
function update_popup(map,props,newContent){
  map.eachLayer(function(i_layer){               
    if (i_layer._id == props.pid){
      i_layer.setPopupContent(newContent)
    }
  })
}

function update_toolTip(map,props,newContent){
  map.eachLayer(function(i_layer){               
    if (i_layer._id == props.pid){
      i_layer.setToolTipContent(newContent,
                                {
                                  direction: 'right',
                                  permanent: true,
                                  sticky: true,
                                  offset: [10, 0],
                                  opacity: 0.65,
                                  className: 'leaflet-tooltip-own' 
                                })
                              }
  })
}

function myScript(){
  //console.log("inside current_page_no::" , current_page_no)
  // keep lastest position
  latest_user_loc_x = user_loc_x 
  latest_user_loc_y = user_loc_y
  //remove previous markers of recent search
 // removeAllMarkers(map,pA)
  //pB = new L.FeatureGroup();
  var search_val = document.getElementById('start').value//.toLowerCase();
  search_val=search_val.replace(/[^a-zA-Z0-9]/g,"")

  //console.log('search ' , search_val,user_loc_x,user_loc_y)
  if (search_val.length>0){            
    dataurl = slug_data_url.replace(/12345/, search_val.toString())
                            .replace(/6677/, user_loc_x)
                            .replace(/8899/, user_loc_y)
                            .replace(/444444/, current_page_no) ; 
    //console.log('1:url', dataurl)
    $('#total_projects_searched').html('Running search [' + search_val + "]")
  }else {
    //all products
    dataurl = base_data_url.replace(/12345/, user_loc_x)
                           .replace(/66778899/, user_loc_y)
                           .replace(/444444/, current_page_no) ;
    //console.log('2:url', dataurl)
    $('#total_projects_searched').html('Running search [all product]')
  }
  //console.log('dataurl ----->>>>>>>>>>>>>>>>>', dataurl)
  // refresh bounds
  bounds = L.latLngBounds()
   // 'new bounds'
  var newLatLng = new L.LatLng(user_loc_y, user_loc_x); 
  bounds.extend(newLatLng)
  while (id_found.length > 0) {
    id_found.pop();
  } // Fastest
  id_found.push('marker')
  //insert_initial()
  // Download GeoJSON data with Ajax
    fetch(dataurl
      ).then(function(resp) {
        return resp.json();
      })
      .then(function(data) {
        console.log('*****  MyScript: data features...', data.features)
        $('.apartments').html("")
        let search_str =search_val
        if (search_val.length ==0)
          search_str =" with no filter"
            
        output_ = "<b style='background-color:yellow'>" + search_str + "</b> [" + data.features.length +"]"

        $('#total_projects_searched').html("Results of " + output_ )
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
            pagedata=props.page_dict
            var content 
            //-- append data------
            let lat_lng = [layer.feature.geometry.coordinates[1],layer.feature.geometry.coordinates[0]]
            bounds.extend(lat_lng)      // Extend LatLngBounds with coordinates
            a_html=append_html(props)                 
           $(a_html).bind("mouseover",function(){                    
              map.flyTo([layer.feature.geometry.coordinates[1],layer.feature.geometry.coordinates[0]],12)
           }).appendTo($('.apartments'));
            //-------------------
           
            anchor_tag =`<a data-toggle="tooltip" data-placement="bottom" title='View Prorduct Details' href="/e/p/d/${props.pid}/">${props.name}</a>`
            if (props.image) {
              content = `<img style="width:100%;height:100px; object-fit: cover;" src="${props.image}"/> </br><p><i style='color:blue'>Shopname</i>: ${props.shopname}</br><i style='color:blue'>Prod</i>: ${anchor_tag} &nbsp;<i class="fas fa-map-marker-alt"></i>${nFormatterdist(props.distance,1)}&nbsp; $${nFormatter(props.price,2)} </p>`;
          
            } else {
              content = `<img                                                       src=""             /> </br><p><i style='color:blue'>Shopname</i>: ${props.shopname}</br><i style='color:blue'>Prod</i>: ${anchor_tag} &nbsp;<i class="fas fa-map-marker-alt"></i>${nFormatterdist(props.distance,1)}&nbsp; $${nFormatter(props.price,2)} </p>`;
          
            }
           
            layer.bindPopup(content)
            newtooltipContent ='<small>$' + nFormatter(props.price,2) +"</small>"
            layer.bindTooltip(
                newtooltipContent,
                {
                  direction: 'right',
                  permanent: true,
                  sticky: true,
                  offset: [10, 0],
                  opacity: 0.65,
                  className: 'leaflet-tooltip-own' 
                });
            layer._id = props.pid
            
            let tag_found=false
            
            pB.eachLayer(function(ll){
               
              if (ll._id == props.pid){
                //console.log('test_lay::::' , ll);
                tag_found=true

                if (!(id_found.includes( props.pid))){
                  id_found.push(props.pid)
                }
              }
            })

           //update map content
            update_popup(map,props,content)
            //methos not working
            //update_toolTip(map,props,newtooltipContent)
           

            if (!tag_found){
                pB.addLayer(layer);
                map.addLayer(layer);
                if (!(id_found.includes(props.pid))){
                  id_found.push(props.pid)
                }
            }
            
      }})//.addTo(map);
      
      pB.eachLayer(function(ll){
        if (!(id_found.includes(ll._id))){
          // new product search drop other products
          // console.log('removed',ll._id)
          map.removeLayer(ll)
          //remove all orphans
          pB.removeLayer(ll)
        }else{
          // console.log('not removed',ll._id) 
        }
      })
      // console.log('::::::>>>2222', id_found)
     
      get_bounds_and_resize_MapView()
     
      //console.log('pagedata>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>',pagedata)
      updatePaging2(pagedata)
    });
    //pagedata = JSON.parse('{{request.session.pagedata|safe}}');
    //call_pagedata()

};
// function addStartPoint(){
//   removeAllMarkers(map,pA)
  
//   for (let i = 0; i < pointsA.length; i++) {
    
//     marker_label= `Standing position <br>${pointsA[i][2]}`
//     marker = L.marker([pointsA[i][0], pointsA[i][1]], {
//                   icon: colorMarker(color[index_a]),
//               }).bindPopup(marker_label);

//     pA.addLayer(marker);
//   }
//   map.addLayer(pA);
// }

function get_transition_metre(bound_m){
 

  let user_latlng1 = L.latLng(user_loc_x, user_loc_y);
  let latest_latlng2 = L.latLng(latest_user_loc_x, latest_user_loc_y);

  let distance = user_latlng1.distanceTo(latest_latlng2)//    / 1000
  
  console.log('Change in distance moved: ', distance , ' map redraws if distance is at least ',bound_m , " metres");
  if (distance > bound_m){
    console.log('User moving beyond ' + bound_m + ' metres  . Going to hit databse to update coordinates')
    return true
  }
  
  return false
}

checkPosition_map_apartment()
//checkPosition_product_details()
$(window).resize(function() {
  checkPosition_map_apartment()
  //checkPosition_product_details()
  
 
 });

function checkPosition_map_apartment() {
    if ( window.matchMedia('(max-width: 767px)').matches)   {// mobile
      $("#setfull_map").css({'display': 'None'})
    }else{
      $("#setfull_map").css({'display': 'block'})
    }
    let isChecked = $('#setfull_map').is(':checked');
     // $('#setfull_map').prop("checked")
    if (isChecked){
      map_full_screen()
    }else {
      resize_match()
    }

    
}
function resize_match(){
  if ( window.matchMedia('(max-width: 767px)').matches)   {// mobile

    $(".apartment-handle").css({'display': 'None'})
    $(".footer-top").css({'display': 'None'})
    $(".map").css({'height':'400px'})
  }else {
    $(".apartment-handle").css({'display': 'block'})
    $(".footer-top").css({'display': 'block'})
    $(".map").css({'height':'400px'})
  }
  if ( window.matchMedia('(max-width: 991px)').matches)   {// mobile
     
      $(".apartment-handle").removeClass('col-md-8')
      $(".apartment-handle").removeClass('col-md-pull-4')
      
    
      $(".apartment-handle").removeClass('col-md-0')
      $(".apartment-handle").removeClass('col-md-pull-12')
      
      //Set 50:50
      $(".apartment-handle").addClass('col-md-6')
      $(".apartment-handle").addClass('col-md-pull-6')

      $(".map-handle").removeClass('col-md-4')
      $(".map-handle").removeClass('col-md-push-4')
      $(".map-handle").removeClass('col-md-12')
      $(".map-handle").removeClass('col-md-push-12') 

      //Set 50:50
      $(".map-handle").addClass('col-md-6')
      $(".map-handle").addClass('col-md-push-6') 
  } else {// wide screen
   
    wide_screen_standard()
  
  }
}
$('#setfull_map').change(function() {

	checkPosition_map_apartment()
});
function wide_screen_standard(){
  var height = $('.map').height();
  //console.log('HH:', height)
  //$(".map").css({'height':'400px'})
  $(".apartment-handle").css({'display': 'block'})
  $(".apartment-handle").removeClass('col-md-6')
  $(".apartment-handle").removeClass('col-md-pull-6')

  $(".apartment-handle").removeClass('col-md-0')
  $(".apartment-handle").removeClass('col-md-pull-12')


  //set 80:40
  $(".apartment-handle").addClass('col-md-8')
  $(".apartment-handle").addClass('col-md-pull-4')

  $(".map-handle").removeClass('col-md-6')
  $(".map-handle").removeClass('col-md-push-6')
  $(".map-handle").removeClass('col-md-12')
  $(".map-handle").removeClass('col-md-push-12') 

  //
  $(".map-handle").addClass('col-md-4')
  $(".map-handle").addClass('col-md-push-4') 
  /* AFTER EFFECT */
  var width = $('#project_div').width()-$('.map').position().left; 
  var height = $('#project_div').height();
 
  if (height>600)
    height=600 
  //reduce height
  if (1.2*width<height)
      height=1.2*width
 
   
  map.invalidateSize();      // should work then
/* 
  I had the same issue in an ionic 4 project. 
  Like suggested in comment with link I needed to use map.invalidateSize() 
  when I rendered the map, as well as when adding/removing markers or any other action for that matter. 
  This didn't help completely. I also had to manually trigger change detection after that. 
  Here's a sample from our code:
  */
}
function map_full_screen(){
      var height = $('.map').height();
      //console.log('HH:', height)
     
      if ( window.matchMedia('(max-width: 767px)').matches)   {// mobile
        $(".footer-top").css({'display': 'None'})
        $(".map").css({'height':'400px'})
      }else {
        $(".footer-top").css({'display': 'block'})
        $(".map").css({'height':'600px'})
      }
     
 
      $(".apartment-handle").css({'display': 'None'})
      $(".apartment-handle").removeClass('col-md-6')
      $(".apartment-handle").removeClass('col-md-pull-6')
      $(".apartment-handle").removeClass('col-md-4')
      $(".apartment-handle").removeClass('col-md-push-4')
     

      $(".apartment-handle").removeClass('col-md-0')
      $(".apartment-handle").removeClass('col-md-pull-12')
      
      
      $(".map-handle").removeClass('col-md-6')
      $(".map-handle").removeClass('col-md-push-4')
      $(".map-handle").removeClass('col-md-push-6')
      $(".map-handle").removeClass('col-md-push-8')
      $(".map-handle").removeClass('col-md-4')

      //
      $(".map-handle").addClass('col-md-12')
      /* AFTER EFFECT */
      var width = $('#project_div').width()-$('.map').position().left; 
      var height = $('#project_div').height();
      if (height>600)
          height=600
      //reduce height
      if (1.2*width<height)
          height=1.2*width

      map.invalidateSize();      // should work then
     
     
}










