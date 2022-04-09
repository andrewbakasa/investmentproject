
function addfeedlotdesignparametersTable(data){
    console.log('addfeedlotdesignparametersTable')
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
                sqm: 'sqm',
                pen_area: 'pen_area',
                sqm_per_cattle: 'sqm_per_cattle',
                total_cattle_per_pen_per_cycle: 'total_cattle_per_pen_per_cycle',
                num_of_months_per_cycle: 'num_of_months_per_cycle',
                cattle_per_pen_per_year: 'cattle_per_pen_per_year',
                num_of_feedlots: 'num_of_feedlots',
                
            };

            
            html_body =''
            $.each(obj, function(key, value) {                                
                x=  `<tr id="feedlotdesignparameters-${key}" >
                    <th scope="row">${value}</th>
                    <td class="feedlotdesignparametersAction feedlotdesignparametersData" name="${key}" >${data['data'][key]}</td>                                                    
                    </tr>`
                html_body = html_body + x
            });
            html_trail= `</tbody>
                </table>
                </div>
                <a href="#" class="btn btn-primary btn-round" data-toggle="modal"
                data-target="#modal_add_model_feedlotdesignparameters"> <i class="fa fa-edit"></i></a>` ;
            
            a_html =html_lead + html_body + html_trail
            $(this).html(a_html)
            //prepare for updating
            console.log('model_id', data['data'].model_id)
            url=`/edit_model_feedlotdesignparameters_ajax/${data['data'].id}/`
            $("#form-feedlotdesignparameters").attr( "data-url",  url)
            $("#feedlotdesignparameters_label").html(`Edit feedlotdesignparameters Parameters: ${data['data'].model_name}`)
            
            
        
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
        const obj = {
            length: 'length',
            width: 'width',
            sqm: 'sqm',
            pen_area: 'pen_area',
            sqm_per_cattle: 'sqm_per_cattle',
            total_cattle_per_pen_per_cycle: 'total_cattle_per_pen_per_cycle',
            num_of_months_per_cycle: 'num_of_months_per_cycle',
            cattle_per_pen_per_year: 'cattle_per_pen_per_year',
            num_of_feedlots: 'num_of_feedlots',
        };


     
        $.each(obj, function(key, value) {
            console.log(value);
            $("#feedlotdesignparametersTable #feedlotdesignparameters-"+ value).children(".feedlotdesignparametersData").each(function() {
                var attr = $(this).attr("name");
                if (attr == value) {
                    a_html =`${data['data'][value]}`;
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
                    if (data['error']=== false) {
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
                    if (data['error']=== false) {
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