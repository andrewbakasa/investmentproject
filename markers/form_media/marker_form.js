// Wait for the map to be initialized
$(window).on('map:init', function(e) {

    map = e.originalEvent.detail.map;
  
    map.on('draw:created', function (e) {
        const coordinates = e.layer._latlng;
        
        call_ajax(coordinates);

    });
    map.on('draw:edited', function (e) {
        var layers =e.layers._layers
        var coordinates;
        Object.keys(layers).forEach(function(key) {

            coordinates = layers[key]._latlng;
            //console.log(coordinates)
        });
        call_ajax(coordinates);
    });

    function call_ajax(coordinates)
    {

        $.ajax({
            type: "GET",
            url: "/riesgo/trabajador/provincia_municipio/ajax/",
            data: {
                'lat': coordinates.lat,
                 'lng': coordinates.lng,
            },
            dataType: "json",
            success: function (response) {

                $('#id_province_id').val(response.province_id); // Select the option with a value of '1'
                $('#id_province_id').trigger('change'); // Notify any JS components that the value changed
            },
            error: function (rs, e) {
                console.log('ERROR obteniendo el bounding box');
            }
        });
    }
});
