function truncChar(str,length){
    var myTruncatedString = str.substring(0,length);              
    if (str.length > myTruncatedString.length){
      return myTruncatedString + "..."
    }
    return myTruncatedString
}

function feedlot_design_module(){
    validate_sqm_per_cattle()
    validate_pen_area() 
    validate_cattle_per_pen_per_year()

}
// $('body').on("change","#id_num_of_months_per_cycle",function(e){
//     validate_cattle_per_pen_per_year()      
// })            
$('body').on("change","#id_total_cattle_per_pen_per_cycle",function(e){
    
    validate_sqm_per_cattle() 
    //validate_cattle_per_pen_per_year()     
})


$('body').on("change","#id_sqm_per_cattle",function(e){
    validate_sqm_per_cattle()             
})



$('body').on("change","#id_length",function(e){
    //validate_pen_area() 
    validate_sqm_per_cattle()    
})


$('body').on("change","#id_width",function(e){
    //validate_pen_area() 
    validate_sqm_per_cattle()         
})



// $('body').on("change","#id_pen_area",function(e){
//     validate_pen_area()           
// })


$('body').on("change","#id_sqm_per_cattle",function(e){
    validate_sqm_per_cattle()           
})

// $('body').on("change","#id_cattle_per_pen_per_year",function(e){
//     validate_cattle_per_pen_per_year()           
// })

function validate_sqm_per_cattle(){
    var pen_area = parseFloat(get_val( $('#id_length').val())) * parseFloat(get_val( $('#id_width').val()))
    var total_cattle_per_pen_per_cycle = $('#id_total_cattle_per_pen_per_cycle').val()
    var sqm_per_cattle = $('#id_sqm_per_cattle').val()
    var valid_output= parseFloat(get_val(pen_area)) / parseFloat(get_val(total_cattle_per_pen_per_cycle))
    valid_output=roundTo(parseFloat(valid_output),2)
    if (valid_output !== sqm_per_cattle){
        $('#id_sqm_per_cattle').val(valid_output)
    }
}

function validate_pen_area(){

    var lenght = $('#id_length').val()
    var width = $('#id_width').val()
    var pen_area = $('#id_pen_area').val()
    var valid_pen_area= parseFloat(get_val(lenght)) * parseFloat(get_val(width))
    valid_pen_area=roundTo(parseFloat(valid_pen_area),2)
    if (valid_pen_area !== pen_area){
        $('#id_pen_area').val(valid_pen_area)
    }
}

function validate_cattle_per_pen_per_year(){

    var cattle_per_pen_per_cycle = $('#id_total_cattle_per_pen_per_cycle').val()
    var num_of_months_per_cycle = $('#id_num_of_months_per_cycle').val()
    var cattle_per_pen_per_year = $('#id_cattle_per_pen_per_year').val()
    var valid_cattle= 12*parseFloat(get_val(cattle_per_pen_per_cycle)) / parseFloat(get_val(num_of_months_per_cycle))
    valid_cattle=roundTo(parseFloat(valid_cattle),2)
    if (valid_cattle !== cattle_per_pen_per_year){
        $('#id_cattle_per_pen_per_year').val(valid_cattle)
    }

}

function addfeedlotdesignparametersTable(data){
    console.log('addfeedlotdesignparametersTable')
    var model_or_data= ''
    if (data['data']){
        model_or_data='data'
    } else if (data['model']){
        model_or_data='model'
    } 
    $("#feedlotdesignparameters_section").children(".view-section").each(function() {
        var attr = $(this).attr("name");
        console.log('before updating',attr )
        if (attr == "my_feedlotdesignparameters_section") {                           
            html_lead=`<table id="feedlotdesignparametersTable" class="table table-striped" >
                <thead>
                </thead>
                <tbody id="feedlotdesignparameters-table-tbody">`
            const obj = {
                length: 'length',
                width: 'width',
               // pen_area: 'pen_area',
                sqm_per_cattle: 'sqm_per_cattle',
                total_cattle_per_pen_per_cycle: 'total_cattle_per_pen_per_cycle',
                num_of_months_per_cycle: 'num_of_months_per_cycle',
                //cattle_per_pen_per_year: 'cattle_per_pen_per_year',
                num_of_feedlots: 'num_of_feedlots',

                construction_cost_per_pen: 'construction_cost_per_pen',
                machinery_cost_per_pen: 'machinery_cost_per_pen',
                building_cost_per_sqm: 'building_cost_per_sqm',
                total_land_sqm: 'total_land_sqm',  
                cost_of_land_per_sqm:'cost_of_land_per_sqm',
                
            };

            
            html_body =''
            $.each(obj, function(key, value) {                                
                x=  `<tr id="feedlotdesignparameters-${key}" >
                    <th scope="row">${value}</th>
                    <td class="feedlotdesignparametersAction feedlotdesignparametersData" name="${key}" >${numberWithCommas(data[model_or_data][key])}</td>                                                    
                    </tr>`
                html_body = html_body + x
            });
            html_trail= `</tbody>
                </table>
                </div>
                <a class="model-edit show-form-update" href="#" data-url="/update_model_feedlotdesignparameters_ajax/${data[model_or_data].id}/" 
                data-target="#modal-edit-product-div" data-toggle="tooltip" data-placement="bottom" 
                title='Edit Feedlot Parameters'><i  class="fas fa-edit"></i>
              </a>` ;
            
            a_html =html_lead + html_body + html_trail
            $(this).html(a_html)
            //prepare for updating
            
            url=`/update_model_feedlotdesignparameters_ajax/${data[model_or_data].id}/`
            $("#form-feedlotdesignparameters").attr( "data-url",  url)
            $("#feedlotdesignparameters_label").html(`Edit feedlotdesignparameters Parameters: ${truncChar(data[model_or_data].model_name,15)}`)
            
            
        
            html_add_check= `<a class="nav-link active show" data-bs-toggle="tab" href="#tab-8">
            <i class="bi bi-check-circle"></i>Feedlot Design</a>`;
            $("#feedlotdesignparameters_tab").html(html_add_check)

            
            // change destination ajax form class
            $("#form-feedlotdesignparameters").attr( "class",  "model-feedlotdesignparameters-edit")                           
            $("#feedlotdesignparameters_accordion_button").removeClass( "section-incomplete")
            $("#feedlotdesignparameters_accordion_button").addClass( "section-complete")
         
        }
    });                   
}               
function updatefeedlotdesignparametersTable(data){
        var model_or_data= ''
        if (data['data']){
            model_or_data='data'
        } else if (data['model']){
            model_or_data='model'
        } 
        const obj = {
            length: 'length',
            width: 'width',
            //
            sqm_per_cattle: 'sqm_per_cattle',
            total_cattle_per_pen_per_cycle: 'total_cattle_per_pen_per_cycle',
            num_of_months_per_cycle: 'num_of_months_per_cycle',
            //cattle_per_pen_per_year: 'cattle_per_pen_per_year',
            num_of_feedlots: 'num_of_feedlots',

            construction_cost_per_pen: 'construction_cost_per_pen',
            machinery_cost_per_pen: 'machinery_cost_per_pen',
            building_cost_per_sqm: 'building_cost_per_sqm',
            total_land_sqm: 'total_land_sqm',  
            cost_of_land_per_sqm:'cost_of_land_per_sqm',
                
        };


     
        $.each(obj, function(key, value) {
            console.log(value);
            $("#feedlotdesignparametersTable #feedlotdesignparameters-"+ value).children(".feedlotdesignparametersData").each(function() {
                var attr = $(this).attr("name");
                if (attr == value) {
                    a_html =`${numberWithCommas(data[model_or_data][value])}`;
                    $(this).html(a_html)
                }
            });
        });            
}
$(document).ready(function(){  
   //FeedLot Design
    $('body').on("submit",".model-feedlotdesignparameters-edit",function(e){
        e.preventDefault();
        var data = new FormData(this);
        var formData
        var form = $(this);
        console.log('Gettting.....') 
        $.ajax({
            url: form.attr('data-url'),
            data : data,
            type: form.attr('method'),
            dataType: 'json',
            processData:false,
            contentType: false,
            beforeSubmit:  $('#submit_feedlotdesignparameters').attr('disabled', 'disabled'),
            success: function(data){
                console.log(data)
                if (data) {
                    if (data['error']=== false ||  data['model'])  {
                        //--update changes
                        updatefeedlotdesignparametersTable(data);
                        checkReadyModel();
                    }							
                $('#submit_feedlotdesignparameters').removeAttr('disabled')
                $('#modal_add_model_feedlotdesignparameters').modal('hide');
                $('.close-modal').click() 
                }
            },
            error: function (exception) {
                console.log(exception.data);
                $('#submit_feedlotdesignparameters').removeAttr('disabled')
            }
        })
        return false;
    })
 
    $('body').on("submit",".model-feedlotdesignparameters-add",function(e){
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
            beforeSubmit:  $('#submit_feedlotdesignparameters').attr('disabled', 'disabled'),
            success: function(data){
                if (data) {
                    if (data['error']=== false ||  data['model'])  {
                        //--update changes
                        addfeedlotdesignparametersTable(data);
                        checkReadyModel();
                    }							
                $('#submit_feedlotdesignparameters').removeAttr('disabled')
                $('#modal_add_model_feedlotdesignparameters').modal('hide');
                $('.close-modal').click() 
                }
            },
            error: function (exception) {
                console.log(exception.data);
                $('#submit_feedlotdesignparameters').removeAttr('disabled')
            }
        })
        return false;
    })
});


$(document).on('shown.bs.modal','.modal',function(e){
    var form_id= $(this).find('form').attr('id')

   if (form_id ==='form-feedlotdesignparameters') {
        feedlot_design_module()  
    }
   
})