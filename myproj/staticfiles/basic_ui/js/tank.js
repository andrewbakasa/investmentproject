 

   
    $(document).ready(function(){        
        
       
        //FishTank Design
        $('body').on("submit",".model-tankdesignparameters-edit",function(e){
            e.preventDefault();
            var data = new FormData(this);
            var formData
            var form = $(this); 
            $.ajax({
                url: form.attr('data-url'),
                data : data,
                type: form.attr('method'),
                dataType: 'json',
                processData:false,
                contentType: false,
                beforeSubmit:  $('#submit_tankdesignparameters').attr('disabled', 'disabled'),
                success: function(data){
                    if (data) {
                        if (data['error']=== false ||  data['model'])  {
                            //--update changes
                            updatetankdesignparametersTable(data);
                            checkReadyModel();
                        }							
                       $('#submit_tankdesignparameters').removeAttr('disabled')
                       $('#modal_add_model_tankdesignparameters').modal('hide');
                       $('.close-modal').click() 
                    }
                },
                error: function (exception) {
                    console.log(exception.data);
                    $('#submit_tankdesignparameters').removeAttr('disabled')
                }
            })
            return false;
        })
         
        $('body').on("submit",".model-tankdesignparameters-add",function(e){
            e.preventDefault();
            var data = new FormData(this);
            var formData
            var form = $(this); 
            $.ajax({
                url: form.attr('data-url'),
                data : data,
                type: form.attr('method'),
                dataType: 'json',
                processData:false,
                contentType: false,
                beforeSubmit:  $('#submit_tankdesignparameters').attr('disabled', 'disabled'),
                success: function(data){
                    if (data) {
                        if (data['error']=== false ||  data['model'])  {
                            //--update changes
                            addtankdesignparametersTable(data);
                            checkReadyModel();
                        }							
                       $('#submit_tankdesignparameters').removeAttr('disabled')
                       $('#modal_add_model_tankdesignparameters').modal('hide');
                       $('.close-modal').click() 
                    }
                },
                error: function (exception) {
                    console.log(exception.data);
                    $('#submit_tankdesignparameters').removeAttr('disabled')
                }
            })
            return false;
        })

    });

    $('body').on("change","#id_volume_of_water",function(e){
        validate_water_volume() 
        validate_density_cubic_metre()      
    })

    
    $('body').on("change","#id_tank_length",function(e){
        validate_water_volume()
        validate_density_cubic_metre()          
    })

    $('body').on("change","#id_tank_width",function(e){
        validate_water_volume() 
        validate_density_cubic_metre()              
    })
       
    $('body').on("change","#id_depth",function(e){
        validate_water_volume() 
        validate_density_cubic_metre()              
    })   
       


    function tank_design_module(){
            validate_fish_per_tank_per_year()
            validate_water_volume() 
            validate_density_cubic_metre()

    }
    function validate_water_volume(){

        var tank_vol = $('#id_volume_of_water').val()
        var tank_length = $('#id_tank_length').val()
        var tank_width = $('#id_tank_width').val()
        var depth = $('#id_depth').val()
        var valid_tank_vol= 1000*parseFloat(get_val(tank_length)) * parseFloat(get_val(tank_width))* parseFloat(get_val(depth))
        valid_tank_vol=Math.round(parseFloat(valid_tank_vol))
        if (valid_tank_vol !== tank_vol){
            $('#id_volume_of_water').val(valid_tank_vol)
        }
    
    }

    $('body').on("change","#id_total_fish_per_tank_per_cycle",function(e){
        validate_density_cubic_metre()              
    })  
    
    $('body').on("change","#id_density_per_cubic_metre",function(e){
        validate_density_cubic_metre()              
    }) 
      
    


    function validate_density_cubic_metre(){

        var fish_tank_cycle = $('#id_total_fish_per_tank_per_cycle').val()
        var vol_water = $('#id_volume_of_water').val()
        var density_per_cubic_metre = $('#id_density_per_cubic_metre').val()
        var valid_density_cm= 1000*parseFloat(get_val(fish_tank_cycle)) / parseFloat(get_val(vol_water))
        valid_density_cm=Math.round(parseFloat(valid_density_cm),1)
        if (valid_density_cm !== density_per_cubic_metre){
            $('#id_density_per_cubic_metre').val(valid_density_cm)
        }
    }

     
    $('body').on("change","#id_fish_per_tank_per_year",function(e){
        validate_fish_per_tank_per_year()              
    }) 
    
    $('body').on("change","#id_tank_num_of_months_per_cycle",function(e){
        validate_fish_per_tank_per_year()              
    }) 
    
    $('body').on("change","#id_total_fish_per_tank_per_cycle",function(e){
        validate_fish_per_tank_per_year()              
    }) 
    
 

       

    function validate_fish_per_tank_per_year(){

        var fish_per_tank_per_year = $('#id_fish_per_tank_per_year').val()
        var total_fish_per_tank_per_cycle = $('#id_total_fish_per_tank_per_cycle').val()
        var num_of_months_per_cycle = $('#id_tank_num_of_months_per_cycle').val()
        var valid_fish_per_tank_per_year= parseFloat(get_val(total_fish_per_tank_per_cycle)) *12/ parseFloat(get_val(num_of_months_per_cycle))
        valid_fish_per_tank_per_year=Math.round(parseFloat(valid_fish_per_tank_per_year),1)
        if (valid_fish_per_tank_per_year !== fish_per_tank_per_year){
            $('#id_fish_per_tank_per_year').val(valid_fish_per_tank_per_year)
        }
    }



    function addtankdesignparametersTable(data){
        console.log('addtankdesignparametersTable')
        var model_or_data= ''
        if (data['data']){
            model_or_data='data'
        } else if (data['model']){
            model_or_data='model'
        } 
        $("#tankdesignparameters_section").children(".view-section").each(function() {
            var attr = $(this).attr("name");
            console.log('before updating',attr )
            if (attr == "my_tankdesignparameters_section") {                           
                html_lead=`<table id="tankdesignparametersTable" class="table table-striped" >
                    <thead>
                    </thead>
                    <tbody id="tankdesignparameters-table-tbody">`
                const obj = {
                    tank_length: 'tank_length',
                    tank_width: 'tank_width',
                    depth: 'depth',
                    volume_of_water: 'volume_of_water',
                    density_per_cubic_metre: 'density_per_cubic_metre',
                    total_fish_per_tank_per_cycle: 'total_fish_per_tank_per_cycle',
                    tank_num_of_months_per_cycle: 'tank_num_of_months_per_cycle',
                    fish_per_tank_per_year: 'fish_per_tank_per_year',
                    num_of_tanks: 'num_of_tanks',

                    purchase_price_tank: 'purchase_price_tank',
                    machinery_cost_per_tank: 'machinery_cost_per_tank',
                    building_cost_per_sqm: 'building_cost_per_sqm',
                    total_land_sqm: 'total_land_sqm',  
                    cost_of_land_per_sqm:'cost_of_land_per_sqm',
                    
                };

                
                html_body =''
                $.each(obj, function(key, value) {                                
                    x=  `<tr id="tankdesignparameters-${key}" >
                        <th scope="row">${value}</th>
                        <td class="tankdesignparametersAction tankdesignparametersData" name="${key}" >${numberWithCommas(data[model_or_data][key])}</td>                                                    
                        </tr>`
                    html_body = html_body + x
                });
                html_trail= `</tbody>
                    </table>
                    </div>
                    <a class="model-edit show-form-update" href="#" data-url="/update_model_tankdesignparameters_ajax/${data[model_or_data].id}/" 
                        data-target="#modal-edit-product-div" data-toggle="tooltip" data-placement="bottom" 
                        title='Edit Tank Parameters'><i  class="fas fa-edit"></i>
                    </a>` ;
                
                a_html =html_lead + html_body + html_trail
                $(this).html(a_html)
                //prepare for updating
                console.log('model_id', data[model_or_data].model_id)
                url=`/update_model_tankdesignparameters_ajax/${data[model_or_data].id}/`
                $("#form-tankdesignparameters").attr( "data-url",  url)
                $("#tankdesignparameters_label").html(`Edit tankdesignparameters Parameters: ${truncChar(data[model_or_data].model_name,15)}`)
                
                html_add_check= `<a class="nav-link active show" data-bs-toggle="tab" href="#tab-8">
                <i class="bi bi-check-circle"></i>Tank Design</a>`;
                $("#tankdesignparameters_tab").html(html_add_check)
                
                // change destination ajax form class
                $("#form-tankdesignparameters").attr( "class",  "model-tankdesignparameters-edit")                           
                $("#tankdesignparameters_accordion_button").removeClass( "section-incomplete")
                $("#tankdesignparameters_accordion_button").addClass( "section-complete")
                
                

                
            }
        });                   
    }               
    function updatetankdesignparametersTable(data){
            var model_or_data= ''
            if (data['data']){
                model_or_data='data'
            } else if (data['model']){
                model_or_data='model'
            } 
            const obj = {
                tank_length: 'tank_length',
                tank_width: 'tank_width',
                depth: 'depth',
                volume_of_water: 'volume_of_water',
                density_per_cubic_metre: 'density_per_cubic_metre',
                total_fish_per_tank_per_cycle: 'total_fish_per_tank_per_cycle',
                tank_num_of_months_per_cycle: 'tank_num_of_months_per_cycle',
                fish_per_tank_per_year: 'fish_per_tank_per_year',
                num_of_tanks: 'num_of_tanks',

                purchase_price_tank: 'purchase_price_tank',
                machinery_cost_per_tank: 'machinery_cost_per_tank',
                building_cost_per_sqm: 'building_cost_per_sqm',
                total_land_sqm: 'total_land_sqm',  
                cost_of_land_per_sqm:'cost_of_land_per_sqm',
            };

           
            
            $.each(obj, function(key, value) {
                console.log(value);
                $("#tankdesignparametersTable #tankdesignparameters-"+ value).children(".tankdesignparametersData").each(function() {
                    var attr = $(this).attr("name");
                    if (attr == value) {
                        a_html =`${numberWithCommas(data[model_or_data][value])}`;
                        $(this).html(a_html)
                    }
                });
            });            
    }

    function truncChar(str,length){
        var myTruncatedString = str.substring(0,length);              
        if (str.length > myTruncatedString.length){
            return myTruncatedString + "..."
        }
        return myTruncatedString
    } 

    $(document).on('shown.bs.modal','.modal',function(e){
        var form_id= $(this).find('form').attr('id')
    
       if (form_id ==='form-tankdesignparameters') {
            tank_design_module()
        }
       
    })