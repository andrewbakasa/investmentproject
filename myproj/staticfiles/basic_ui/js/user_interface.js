
 $('body').on("click",".close-modal",function(e){
    e.stopPropagation()
  //   Was giving error. Could not close modal forma after clkick x or Close button
  //  2 hours to solve. eish!! 27 March 2022 from 1000hrs-1215hrs
  // Glory be to Jesus
  //   console.log('Click  close modal class')
    $('#modal-usermodel').modal('hide');
    //$('.close-modal').click()

})


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

function checkReadyModel() {
    var att = $('#run_simu').css("display");
    if(att=='block'){
        //console.log('block found', att) 
        return  
    }
    //console.log('check-display-attr', att)
    var formData = {
        csrfmiddlewaretoken: csrftoken,
        contentType: 'application/x-www-form-urlencoded',
        encode: true,
    };
    
    $.ajax({
        type: 'POST',
        url: check_url_ajax,
        encode: true,
        contentType: 'application/x-www-form-urlencoded',
        crossDomain: false,
        dataType: 'json',
        data: formData,     // our data object
        success: function(data){
            if (data.data) {
                $('#run_simu').css("display", "block");
                $('#progress_iter').css("display", "none");
                
            }else if (data.status){
                $('#progress_iter').text(data.status);
            }
        },
        error: function (exception) {
            console.log(exception);
           
        }
    })
    return false;
}

var csrftoken = getToken('csrftoken');
$(document).ready(function(){
       $('.progressBar').css("display", "none"); 
       checkReadyModel() 
       //------LOAD THE FORM ON MODAL DIV----------
       $('body').on('click', '.show-form-update', function(){
            var btn = $(this);// fix button  delay
          
            $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType:'json',
            beforeSend: function(){
                $('#modal-usermodel').modal('show');
            },
            
            success: function(data){
                $('#modal-usermodel .modal-content').html(data.html_form);
            }
            });

        })

    
        
       $('body').on('click', '.show-form-download', function(){
        
           // check if requirement are satified else return
           // clear progrees bar if refreshes
            $('.progressBar').css("display", "none");
            var btn = $(this);// fix button  delay
            var url =  btn.attr("data-url")
            //btn.fadeOut(1000).fadeIn(1000).hide(1000)
            
            const intervalLength = 1000//'{{interva_l}}'; 
            console.log('intervalLength', intervalLength)                 
            var interval= setInterval(progressTimer, intervalLength);
            $('#run_simu').css('display', 'none');
            setTimeout(function () {                       
                $('.progressBar').css("display", "block");                         
            }, 1.5*intervalLength);    
            $.ajax({
                type: 'GET',
                    cache: false,
                    url: url,                        
                    xhrFields: {
                        // make sure the response knows we're expecting a binary type in return.
                        // this is important, without it the excel file is marked corrupted.
                        responseType: 'arraybuffer'
                    }
                        
            }).done(function (data, status, xmlHeaderRequest) {
                        var downloadLink = document.createElement('a');
                        var blob = new Blob([data],
                            {
                                type: xmlHeaderRequest.getResponseHeader('Content-Type')
                            });
                        var url = window.URL || window.webkitURL;
                        var downloadUrl = url.createObjectURL(blob);
                        
                        var fileName = $('#user_doc_name').val()//'{{user_doc_name}}';

                        if (typeof window.navigator.msSaveBlob !== 'undefined') {
                            window.navigator.msSaveBlob(blob, fileName);
                        } else {
                            if (fileName) {
                                if (typeof downloadLink.download === 'undefined') {
                                    window.location = downloadUrl;
                                } else {
                                    downloadLink.href = downloadUrl;
                                    downloadLink.download = fileName;
                                    document.body.appendChild(downloadLink);
                                    downloadLink.click();
                                }
                            } else {
                                window.location = downloadUrl;
                            }

                            setTimeout(function () {
                                url.revokeObjectURL(downloadUrl);
                                //enable
                                clearInterval(interval)
                                // $('#run_simu').prop('disabled', false);
                                $('.progressBar').css("display", "none"); 
                                $('#run_simu').fadeIn(1000)
                                // console.log('showing run simu')
                                //$('#run_simu').css("display", "block");
                            },100);
                        }
                    });
        });


        
        function progressTimer() {
                let progress = 0;
                const progressBar = document.querySelector('.progressBar');
                const bar = progressBar.querySelector('.bar')
                const progressBarText = progressBar.querySelector('h3');

                var url2 ='/check_count_ajax'
                var formData = {
                    csrfmiddlewaretoken: csrftoken,
                    contentType: 'application/x-www-form-urlencoded',
                    encode: true,
                };
                $.ajax({
                    type: 'POST',
                    url: url2,
                    encode: true,
                    contentType: 'application/x-www-form-urlencoded',
                    crossDomain: false,
                    dataType: 'json',
                    data: formData,     // our data object
                    
                    success:function(response){
                        if (parseInt(response.data.progress) >= 100) {
                            console.log('100% mark reached')
                            bar.style.width = '100%';
                            progressBarText.innerHTML = `Now downloading. Please wait...`;
                        } else { 
                            if (parseInt(response.data.progress) == 0){ 
                                //preararing data  
                                if (progressBarText.innerHTML == `Preparing data...`){
                                    progressBarText.innerHTML = `Preparing data.`;
                                }else if((progressBarText.innerHTML == `Preparing data..`)){
                                    progressBarText.innerHTML = `Preparing data...`;
                                }else if((progressBarText.innerHTML == `Preparing data.`)){
                                    progressBarText.innerHTML = `Preparing data..`;
                                } else {
                                    progressBarText.innerHTML = `Preparing data.`;
                                }
                            //Run simulation   
                            }else{
                                progressBarText.innerHTML = `${response.data.progress} %`;
                            }
                            bar.style.width = response.data.progress + '%';
                           
                        }
                    }
                })
            }
                  
         

        function progess_callback (){
            const intervalLength = 5000;
            var url ='/check_count_ajax'
            let progress = 0;
            const progressBar = document.querySelector('.progressBar');
            const bar = progressBar.querySelector('.bar')
            const progressBarText = progressBar.querySelector('h3');
            const interval = setInterval(() => {
                $.ajax({
                    type: 'POST',
                    url: url,
                    data: {
                        userInstance : $('input[name=uniqueUserInstance]').val(),
                        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                    },
                    success:function(response){
                        // Do visualization stuff then check if complete
                        //console.log(response,response.data )
                        if (parseInt(response.progress) >= 100) {
                            console.log('100% mark reached')
                            clearInterval(interval);
                            bar.style.width = '100%';
                            progressBarText.innerHTML = '100%';
                        } else {
                            bar.style.width = response.data.progress + '%';
                            progressBarText.innerHTML = `${response.data.progress} %`;
                        }
                    }
                });
            }, intervalLength);   
        }

        //Prices
        $('body').on("submit",".model-prices-edit",function(e){
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
                beforeSubmit:  $('#submit_prices').attr('disabled', 'disabled'),
                success: function(data){
                    if (data) {
                        if (data['error']=== false ||  data['model']) {
                            //--update changes
                            updatePricesTable(data);
                            checkReadyModel();
                        }
                        					
                       $('#submit_prices').removeAttr('disabled')
                       $('#modal_add_model_prices').modal('hide');
                       $('.close-modal').click() 
                    }
                },
                error: function (exception) {
                    console.log(exception);
                    $('#submit_prices').removeAttr('disabled')
                }
            })
            return false;
        })

        $('body').on("submit",".model-prices-add",function(e){
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
                beforeSubmit:  $('#submit_prices').attr('disabled', 'disabled'),
                success: function(data){
                    if (data) {
                        if (data['error']=== false ||  data['model']) {
                            //--update changes
                            addPricesTable(data);
                            checkReadyModel();
                        }							
                       $('#submit_prices').removeAttr('disabled')
                       $('#modal_add_model_prices').modal('hide');
                       $('.close-modal').click() 
                    }
                },
                error: function (exception) {
                    console.log(exception);
                    $('#submit_prices').removeAttr('disabled')
                }
            })
            return false;
        })


        function addPricesTable(data){
            console.log('addPricesTable')
            var model_or_data= ''
            if (data['data']){
                model_or_data='data'
            } else if (data['model']){
                model_or_data='model'
            } 
            $("#prices_section").children(".view-section").each(function() {
                var attr = $(this).attr("name");
                console.log('before updating',attr )
                if (attr == "my_prices_section") {
                    a_html=`<table id="pricesTable" class="table table-striped" >
                        <thead>
                        </thead>
                        <tbody id="prices-table-tbody">
                            <tr id="prices-title" >
                                <th scope="row">Title</th>
                                <td class="pricesAction pricesData" name="title" >${data[model_or_data].title}</td>                                                    
                            </tr>
                            <tr id="prices-base-price" >
                                <th scope="row">Base Price(per ton)</th>
                                <td class="pricesAction pricesData"  name="base_price">${data[model_or_data].base_price}</td>                                                    
                            </tr>
                            <tr id="prices-change-in-price" >
                                <th scope="row">Change In Price (%)</th>
                                <td class="pricesAction pricesData"  name="change_in_price">${data[model_or_data].change_in_price}</td>                                                    
                            </tr>
                        </tbody>
                    </table>
                    </div>
                    <a class="model-edit show-form-update" href="#" data-url="/update_model_prices_ajax/${data[model_or_data].id}/" 
                        data-target="#modal-edit-product-div" data-toggle="tooltip" data-placement="bottom" 
                        title='Edit Prices'><i  class="fas fa-edit"></i>
                    </a>` ;
                    //prepare for updating
                    $(this).html(a_html)
                    
                    url=`/update_model_prices_ajax/${data[model_or_data].id}/`                     
                   
                   
                    $("#form-prices").attr( "data-url",  url)
                    $("#prices_label").html(`Edit Prices: ${truncChar(data[model_or_data].model_name,15)}`)
                    
                    html_add_check= `<a class="nav-link active show" data-bs-toggle="tab" href="#tab-2">
                    <i class="bi bi-check-circle"></i> Prices Details</a>`;
                    $("#price_tab").html(html_add_check)
                    
                    // change destination ajax form class
                    $("#form-prices").attr( "class",  "model-prices-edit")
                    $("#prices_accordion_button").removeClass( "section-incomplete")
                    $("#prices_accordion_button").addClass( "section-complete")

                   
                    
                }
            });

           
        }
       
        function updatePricesTable(data){
            // const obj = {
            //     two: 'title',
            //     three: 'base-price',
            //     four: 'change-in-price',
            //     };
            var model_or_data= ''
            if (data['data']){
                model_or_data='data'
            } else if (data['model']){
                model_or_data='model'
            } 
            
            $("#pricesTable #prices-title").children(".pricesData").each(function() {
                var attr = $(this).attr("name");
                if (attr == "title") {
                    a_html =`${data[model_or_data]['title']}`;
                    $(this).html(a_html)
                }
            });

            $("#pricesTable #prices-base-price").children(".pricesData").each(function() {
                var attr = $(this).attr("name");
                if  (attr == "base_price")  {
                    $(this).text('$' + numberWithCommas(data[model_or_data].base_price));
                }
            });
         
            $("#pricesTable #prices-change-in-price").children(".pricesData").each(function() {
                var attr = $(this).attr("name");
                if (attr == "change_in_price")  {
                    $(this).text(data[model_or_data].change_in_price);
                    
                }
            });

           

        }

      
   
        
        $('body').on("submit",".model-timing-assumptions-edit",function(e){
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
                beforeSubmit:  $('#submit_timing_assumptions').attr('disabled', 'disabled'),
                success: function(data){
                    if (data) {
                        if (data['error']=== false ||  data['model'])  {
                           //--update changes
                            updateTimingTable(data);
                            checkReadyModel();
                        }
                        $('#modal-usermodel').modal('hide');
                        $('#submit_timing_assumptions').removeAttr('disabled')
                        $('#modal_add_edit_model_timing_assumptions').modal('hide');
                        $('.close-modal').click() 
                    }
                },
                error: function (exception) {
                    console.log(exception);
                    $('#submit_timing_assumptions').removeAttr('disabled')
                }
            })
            return false;
        })

        $('body').on("submit",".model-timing-assumptions-add",function(e){
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
                beforeSubmit:  $('#submit_timing_assumptions').attr('disabled', 'disabled'),
                success: function(data){
                    if (data) {
                        
                        if (data['error']=== false ||  data['model'])  {
                            //--update changes
                          
                            addTimingTable(data);
                            checkReadyModel();
                        }							
                       $('#submit_timing_assumptions').removeAttr('disabled')
                       $('#modal_add_edit_model_timing_assumptions').modal('hide');
                       $('.close-modal').click() 
                    }
                },
                error: function (exception) {
                    console.log(exception);
                    $('#submit_timing_assumptions').removeAttr('disabled')
                }
            })
            return false;
        })
        function addTimingTable(data){
            console.log('addTimingTable')
            var model_or_data= ''
            if (data['data']){
                model_or_data='data'
            } else if (data['model']){
                model_or_data='model'
            } 
            $("#timing_assumptions_section").children(".view-section").each(function() {
                var attr = $(this).attr("name");
                if (attr == "my_timing_assumptions_section") {                           
                    html_lead=`<table id="timingTable" class="table table-striped" >
                        <thead>
                        </thead>
                        <tbody id="timing-table-tbody">`
                    const obj = {
                        base_period: 'Base Period',
                        construction_start_year: 'Construction Start Year',
                        construction_len: 'Construction Length',
                        construction_year_end: 'Construction Year End',
                        operation_start_year: 'Operation Start Year',
                        operation_duration: 'Operation Duration',
                        operation_end: 'Operation End',
                        number_of_months_in_a_year: '# of months in year'
                    };
                    html_body =''
                    $.each(obj, function(key, value) { 
                        
                                                    
                        x=  `<tr id="timing-${key}" >
                            <th scope="row">${value}</th>
                            <td class="timingAction timingData" name="${key}" >${data[model_or_data][key]}</td>                                                    
                            </tr>`
                        html_body = html_body + x
                    });
                    html_trail= `</tbody>
                        </table>
                        </div>
                        <a class="model-edit show-form-update" href="#" data-url="/update_model_timing_assumptions_ajax/${data[model_or_data].id}/" 
                          data-target="#modal-edit-product-div" data-toggle="tooltip" data-placement="bottom" 
                          title='Edit Timing Assumptions'><i  class="fas fa-edit"></i>
                        </a>` ;
                    a_html =html_lead + html_body + html_trail
                    $(this).html(a_html)
                    //prepare for updating
                    
                    url=`/update_model_timing_assumptions_ajax/${data[model_or_data].id}/`
                     
                    $("#form-timing-assumptions").attr( "data-url",  url)
                    $("#timing_assumptions_label").html(`Edit Timing Assumptions: ${truncChar(data[model_or_data].model_name,15)}`)
                    
                   
                    html_add_check= `<a class="nav-link active show" data-bs-toggle="tab" href="#tab-1">
                           <i class="bi bi-check-circle"></i> Timing Assumptions</a>`;
                    $("#timing_assumption_tab").html(html_add_check)
                    // change destination ajax form class
                    $("#form-timing-assumptions").attr( "class",  "model-timing-assumptions-edit")
                    $("#timing_assumptions_accordion_button").removeClass( "section-incomplete")
                    $("#timing_assumptions_accordion_button").addClass( "section-complete")
                    
                   
                                          
                }
            }); 

        }  
        
      
    
        function updateTimingTable(data){
                const obj = {
                two: 'base_period',
                three: 'construction_start_year',
                four: 'construction_len',
                five: 'construction_year_end',
                six: 'operation_start_year',
                seven: 'operation_duration',
                eight: 'operation_end',
                nine: 'number_of_months_in_a_year'
                };

                $.each(obj, function(key, value) {
                    $("#timingTable #timing-"+ value).children(".timingData").each(function() {
                        var attr = $(this).attr("name");
                        if (attr == value) {
                            if (data['data']){
                                a_html =`${data['data'][value]}`;
                                $(this).html(a_html)
                            }else if(data['model']){
                                a_html =`${data['model'][value]}`;
                                $(this).html(a_html)
                            }                            
                        }
                    });
                });            
        }

         // Depreciation
         $('body').on("submit",".model-depreciation-edit",function(e){
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
                beforeSubmit:  $('#submit_depreciation').attr('disabled', 'disabled'),
                success: function(data){
                    if (data) {
                        if (data['error']=== false ||  data['model'])  {
                            //--update changes
                            updateDepreciationTable(data);
                            checkReadyModel();
                        }
                       $('#modal-usermodel').modal('hide'); 							
                       $('#submit_depreciation').removeAttr('disabled')
                       $('#modal_add_model_depreciation').modal('hide');
                       $('.close-modal').click() 
                    }
                },
                error: function (exception) {
                    console.log(exception);
                    $('#submit_depreciation').removeAttr('disabled')
                }
            })
            return false;
        })

        $('body').on("submit",".model-depreciation-add",function(e){
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
                beforeSubmit:  $('#submit_depreciation').attr('disabled', 'disabled'),
                success: function(data){
                    if (data) {
                        if (data['error']=== false || data['model']) {
                            //--update changes
                            addDepreciationTable(data);
                            checkReadyModel();
                        }							
                       $('#submit_depreciation').removeAttr('disabled')
                       $('#modal_add_model_depreciation').modal('hide');
                       $('.close-modal').click() 
                    }
                },
                error: function (exception) {
                    console.log(exception);
                    $('#submit_depreciation').removeAttr('disabled')
                }
            })
            return false;
        })
        function addDepreciationTable(data){
            console.log('addDepreciationTable')
            var model_or_data= ''
            if (data['data']){
                model_or_data='data'
            } else if (data['model']){
                model_or_data='model'
            } 
            $("#depreciation_section").children(".view-section").each(function() {
                var attr = $(this).attr("name");
                //console.log('before updating',attr )
                if (attr == "my_depreciation_section") {                           
                    html_lead=`<table id="depreciationTable" class="table table-striped" >
                        <thead>
                        </thead>
                        <tbody id="depreciation-table-tbody">`
                    const obj = {
                        economic_life_of_machinery: 'economic_life_of_machinery',
                        economic_life_of_buildings: 'economic_life_of_buildings',
                        tax_life_of_machinery: 'tax_life_of_machinery',
                        tax_life_of_buildings: 'tax_life_of_buildings',
                        tax_life_of_soft_capital_costs: 'tax_life_of_soft_capital_costs',
                       
                    };

                    
                    html_body =''
                    $.each(obj, function(key, value) {                                
                        x=  `<tr id="depreciation-${key}" >
                            <th scope="row">${value}</th>
                            <td class="depreciationAction depreciationData" name="${key}" >${data[model_or_data][key]}</td>                                                    
                            </tr>`
                        html_body = html_body + x
                    });
                    html_trail= `</tbody>
                        </table>
                        </div>
                        <a class="model-edit show-form-update" href="#" data-url="/update_model_depreciation_ajax/${data[model_or_data].id}/" 
                            data-target="#modal-edit-product-div" data-toggle="tooltip" data-placement="bottom" 
                            title='Edit Depreciation'><i  class="fas fa-edit"></i>
                        </a> ` ;
                    
                    a_html =html_lead + html_body + html_trail
                    $(this).html(a_html)
                    //prepare for updating
                    console.log('model_id', data[model_or_data].model_id)
                    url=`/update_model_depreciation_ajax/${data[model_or_data].id}/`
                    $("#form-depreciation").attr( "data-url",  url)
                    $("#depreciation_label").html(`Edit depreciation Assumptions: ${truncChar(data[model_or_data].model_name,15)}`)
                    
                    html_add_check= `<a class="nav-link active show" data-bs-toggle="tab" href="#tab-4">
                    <i class="bi bi-check-circle"></i> Depreciation Details</a>`;
                    $("#depreciation_tab").html(html_add_check)
                    
                    // change destination ajax form class
                    $("#form-depreciation").attr( "class",  "model-depreciation-edit")
                    $("#depreciation_accordion_button").removeClass( "section-incomplete")
                    $("#depreciation_accordion_button").addClass( "section-complete") 
                    
                    

                  
                }
            });                   
        }               
        function updateDepreciationTable(data){
                var model_or_data= ''
                if (data['data']){
                    model_or_data='data'
                } else if (data['model']){
                    model_or_data='model'
                } 
                const obj = {
                    economic_life_of_machinery: 'economic_life_of_machinery',
                    economic_life_of_buildings: 'economic_life_of_buildings',
                    tax_life_of_machinery: 'tax_life_of_machinery',
                    tax_life_of_buildings: 'tax_life_of_buildings',
                    tax_life_of_soft_capital_costs: 'tax_life_of_soft_capital_costs',
                };

                $.each(obj, function(key, value) {
                    //console.log(value);
                    $("#depreciationTable #depreciation-"+ value).children(".depreciationData").each(function() {
                        var attr = $(this).attr("name");
                        if (attr == value) {
                            a_html =`${data[model_or_data][value]}`;
                            $(this).html(a_html)                                 
                        }
                    });
                });            
        }
         
        // Taxes
        $('body').on("submit",".model-taxes-edit",function(e){
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
                beforeSubmit:  $('#submit_taxes').attr('disabled', 'disabled'),
                success: function(data){
                    if (data) {
                        if (data['error']=== false || data['model']) {
                            //--update changes
                            updatetaxesTable(data);
                            checkReadyModel();
                        }							
                       $('#submit_taxes').removeAttr('disabled')
                       $('#modal_add_model_taxes').modal('hide');
                       $('.close-modal').click() 
                    }
                },
                error: function (exception) {
                    console.log(exception);
                    $('#submit_taxes').removeAttr('disabled')
                }
            })
            return false;
        })

        $('body').on("submit",".model-taxes-add",function(e){
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
                beforeSubmit:  $('#submit_taxes').attr('disabled', 'disabled'),
                success: function(data){
                    if (data) {
                        if (data['error']=== false || data['model']) {
                            //--update changes
                            addtaxesTable(data);
                            checkReadyModel();
                        }							
                       $('#submit_taxes').removeAttr('disabled')
                       $('#modal_add_model_taxes').modal('hide');
                       $('.close-modal').click() 
                    }
                },
                error: function (exception) {
                    console.log(exception);
                    $('#submit_taxes').removeAttr('disabled')
                }
            })
            return false;
        })
        function addtaxesTable(data){
            console.log('addtaxesTable')
            var model_or_data= ''
            if (data['data']){
                model_or_data='data'
            } else if (data['model']){
                model_or_data='model'
            } 
            $("#taxes_section").children(".view-section").each(function() {
                var attr = $(this).attr("name");
                console.log('before updating',attr )
                if (attr == "my_taxes_section") {                           
                    html_lead=`<table id="taxesTable" class="table table-striped" >
                        <thead>
                        </thead>
                        <tbody id="taxes-table-tbody">`
                    const obj = {
                        import_duty: 'import_duty',
                        sales_tax: 'sales_tax',
                        corporate_income_tax: 'corporate_income_tax'
                    };

                    
                    html_body =''
                    $.each(obj, function(key, value) {                                
                        x=  `<tr id="taxes-${key}" >
                            <th scope="row">${value}</th>
                            <td class="taxesAction taxesData" name="${key}" >${data[model_or_data][key]}</td>                                                    
                            </tr>`
                        html_body = html_body + x
                    });
                    html_trail= `</tbody>
                        </table>
                        </div>
                        <a class="model-edit show-form-update" href="#" data-url="/update_model_taxes_ajax/${data[model_or_data].id}/" 
                        data-target="#modal-edit-product-div" data-toggle="tooltip" data-placement="bottom" 
                        title='Edit Taxes'><i  class="fas fa-edit"></i>
                      </a>` ;
                    
                    a_html =html_lead + html_body + html_trail
                    $(this).html(a_html)
                    //prepare for updating
                    console.log('model_id', data[model_or_data].model_id)
                    url=`/update_model_taxes_ajax/${data[model_or_data].id}/`
                    $("#form-taxes").attr( "data-url",  url)
                    $("#taxes_label").html(`Edit taxes Assumptions: ${truncChar(data[model_or_data].model_name,15)}`)
                    // change destination ajax form class
                    $("#form-taxes").attr( "class",  "model-taxes-edit")
                    
                    $("#taxes_accordion_button").removeClass( "section-incomplete")
                    $("#taxes_accordion_button").addClass( "section-complete") 

                    html_add_check= `<a class="nav-link active show" data-bs-toggle="tab" href="#tab-5">
                    <i class="bi bi-check-circle"></i> Taxes Details</a>`;
                    $("#taxes_tab").html(html_add_check)

                  
                  
                }
            });                   
        }               
        function updatetaxesTable(data){
                const obj = {
                    import_duty: 'import_duty',
                    sales_tax: 'sales_tax',
                    corporate_income_tax: 'corporate_income_tax'
                };

                $.each(obj, function(key, value) {
                    console.log(value);
                    $("#taxesTable #taxes-"+ value).children(".taxesData").each(function() {
                        var attr = $(this).attr("name");
                        if (attr == value) {
                            if (data['data']){
                                a_html =`${data['data'][value]}`;
                                $(this).html(a_html)
                            }else if(data['model']){
                                a_html =`${data['model'][value]}`;
                                $(this).html(a_html)
                            }     
                        }
                    });
                });            
        }
        
         // Financing
         $('body').on("submit",".model-financing-edit",function(e){
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
                beforeSubmit:  $('#submit_financing').attr('disabled', 'disabled'),
                success: function(data){
                    console.log('Finance:', data)
                    if (data) {
                        if (data['error']=== false || data['model']) {
                            //--update changes
                            updatefinancingTable(data);
                            checkReadyModel();
                        }							
                       $('#submit_financing').removeAttr('disabled')
                       $('#modal_add_model_financing').modal('hide');
                       $('.close-modal').click() 
                    }
                },
                error: function (exception) {
                    console.log(exception);
                    $('#submit_financing').removeAttr('disabled')
                }
            })
            return false;
        })

        $('body').on("submit",".model-financing-add",function(e){
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
                beforeSubmit:  $('#submit_financing').attr('disabled', 'disabled'),
                success: function(data){
                    console.log('Finance:', data)
                    if (data) {
                        if (data['error']=== false || data['model']) {
                            //--update changes
                            addfinancingTable(data);
                            checkReadyModel();
                        }							
                       $('#submit_financing').removeAttr('disabled')
                       $('#modal_add_model_financing').modal('hide');
                       $('.close-modal').click() 
                    }
                },
                error: function (exception) {
                    console.log(exception);
                    $('#submit_financing').removeAttr('disabled')
                }
            })
            return false;
        })
        function addfinancingTable(data){
            console.log('addfinancingTable')
            var model_or_data= ''
            if (data['data']){
                model_or_data='data'
            } else if (data['model']){
                model_or_data='model'
            } 
            $("#financing_section").children(".view-section").each(function() {
                var attr = $(this).attr("name");
                console.log('before updating',attr )
                if (attr == "my_financing_section") {                           
                    html_lead=`<table id="financingTable" class="table table-striped" >
                        <thead>
                        </thead>
                        <tbody id="financing-table-tbody">`
                    const obj = {
                        real_interest_rate: 'real_interest_rate',
                        risk_premium: 'risk_premium',
                        num_of_installments: 'num_of_installments',
                        grace_period: 'grace_period',
                        equity: 'equity',
                        senior_debt: 'senior_debt'
                    };

                    
                    html_body =''
                    $.each(obj, function(key, value) {                                
                        x=  `<tr id="financing-${key}" >
                            <th scope="row">${value}</th>
                            <td class="financingAction financingData" name="${key}" >${data[model_or_data][key]}</td>                                                    
                            </tr>`
                        html_body = html_body + x
                    });
                    html_trail= `</tbody>
                        </table>
                        </div>
                        <a class="model-edit show-form-update" href="#" data-url="/update_model_financing_ajax/${data[model_or_data].id}/" 
                            data-target="#modal-edit-product-div" data-toggle="tooltip" data-placement="bottom" 
                            title='Edit Financing'><i  class="fas fa-edit"></i>
                        </a>` ;
                    
                    a_html =html_lead + html_body + html_trail
                    $(this).html(a_html)
                    //prepare for updating
                    console.log('model_id', data[model_or_data].model_id)
                    url=`/update_model_financing_ajax/${data[model_or_data].id}/` 
                    $("#form-financing").attr( "data-url",  url)
                    $("#financing_label").html(`Edit Financing Parameters: ${truncChar(data[model_or_data].model_name,15)}`)
                    
                    html_add_check= `<a class="nav-link active show" data-bs-toggle="tab" href="#tab-3">
                    <i class="bi bi-check-circle"></i> Financing Details</a>`;
                    $("#financing_tab").html(html_add_check)

                    // change destination ajax form class
                    $("#form-financing").attr( "class",  "model-financing-edit") 
                    $("#financing_accordion_button").removeClass( "section-incomplete")
                    $("#financing_accordion_button").addClass( "section-complete") 
                    
                    
                  
                    
                }
            });                   
        }               
        function updatefinancingTable(data){
                const obj = {
                    real_interest_rate: 'real_interest_rate',
                    risk_premium: 'risk_premium',
                    num_of_installments: 'num_of_installments',
                    grace_period: 'grace_period',
                    equity: 'equity',
                    senior_debt: 'senior_debt'
                };

                $.each(obj, function(key, value) {
                    console.log(value);
                    $("#financingTable #financing-"+ value).children(".financingData").each(function() {
                        var attr = $(this).attr("name");
                        if (attr == value) {
                            if (data['data']){
                                a_html =`${data['data'][value]}`;
                                $(this).html(a_html)
                            }else if(data['model']){
                                a_html =`${data['model'][value]}`;
                                $(this).html(a_html)
                            }                            
                        }
                    });
                });            
        }

        // Working Capital
        $('body').on("submit",".model-workingcapital-edit",function(e){
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
                beforeSubmit:  $('#submit_workingcapital').attr('disabled', 'disabled'),
                success: function(data){
                    if (data) {
                        if (data['error']=== false || data['model']) {
                            //--update changes
                            updateworkingcapitalTable(data);
                            checkReadyModel();
                        }							
                       $('#submit_workingcapital').removeAttr('disabled')
                       $('#modal_add_model_workingcapital').modal('hide');
                       $('.close-modal').click() 
                    }
                },
                error: function (exception) {
                    console.log(exception);
                    $('#submit_workingcapital').removeAttr('disabled')
                }
            })
            return false;
        })

        $('body').on("submit",".model-workingcapital-add",function(e){
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
                beforeSubmit:  $('#submit_workingcapital').attr('disabled', 'disabled'),
                success: function(data){
                    if (data) {
                        if (data['error']=== false || data['model']) {
                            //--update changes
                            addworkingcapitalTable(data);
                            checkReadyModel();
                        }							
                       $('#submit_workingcapital').removeAttr('disabled')
                       $('#modal_add_model_workingcapital').modal('hide');
                       $('.close-modal').click() 
                    }
                },
                error: function (exception) {
                    console.log(exception);
                    $('#submit_workingcapital').removeAttr('disabled')
                }
            })
            return false;
        })
        function addworkingcapitalTable(data){
            console.log('addworkingcapitalTable')
            var model_or_data= ''
            if (data['data']){
                model_or_data='data'
            } else if (data['model']){
                model_or_data='model'
            } 
            $("#workingcapital_section").children(".view-section").each(function() {
                var attr = $(this).attr("name");
                console.log('before updating',attr )
                if (attr == "my_workingcapital_section") {                           
                    html_lead=`<table id="workingcapitalTable" class="table table-striped" >
                        <thead>
                        </thead>
                        <tbody id="workingcapital-table-tbody">`
                    const obj = {
                        accounts_receivable: 'accounts_receivable',
                        accounts_payable: 'accounts_payable',
                        cash_balance: 'cash_balance',
                    };

                    
                    html_body =''
                    $.each(obj, function(key, value) {                                
                        x=  `<tr id="workingcapital-${key}" >
                            <th scope="row">${value}</th>
                            <td class="workingcapitalAction workingcapitalData" name="${key}" >${data[model_or_data][key]}</td>                                                    
                            </tr>`
                        html_body = html_body + x
                    });
                    html_trail= `</tbody>
                        </table>
                        </div>
                        <a class="model-edit show-form-update" href="#" data-url="/update_model_working_capital_ajax/${data[model_or_data].id}/" 
                          data-target="#modal-edit-product-div" data-toggle="tooltip" data-placement="bottom" 
                          title='Edit Timing Assumptions'><i  class="fas fa-edit"></i>
                        </a>` ;
                    
                    a_html =html_lead + html_body + html_trail
                    $(this).html(a_html)
                    //prepare for updating
                    console.log('model_id', data[model_or_data].model_id)
                    url=`/update_model_working_capital_ajax/${data[model_or_data].id}/`
                    $("#form-workingcapital").attr( "data-url",  url)
                    $("#workingcapital_label").html(`Edit workingcapital Parameters: ${truncChar(data[model_or_data].model_name,15)}`)
                    // change destination ajax form class
                    $("#form-workingcapital").attr( "class",  "model-workingcapital-edit")
                    
                    $("#workingcapital_accordion_button").removeClass( "section-incomplete")
                    $("#workingcapital_accordion_button").addClass( "section-complete")
                    
                    

                    html_add_check= `<a class="nav-link active show" data-bs-toggle="tab" href="#tab-6">
                    <i class="bi bi-check-circle"></i>Working Capital</a>`;
                    $("#workingcapital_tab").html(html_add_check)
                    

                }
            });                   
        }               
        function updateworkingcapitalTable(data){
                const obj = {
                    accounts_receivable: 'accounts_receivable',
                    accounts_payable: 'accounts_payable',
                    cash_balance: 'cash_balance',
                };
             
                $.each(obj, function(key, value) {
                    console.log(value);
                    $("#workingcapitalTable #workingcapital-"+ value).children(".workingcapitalData").each(function() {
                        var attr = $(this).attr("name");
                        if (attr == value) {
                            if (data['data']){
                                a_html =`${data['data'][value]}`;
                                $(this).html(a_html)
                            }else if(data['model']){
                                a_html =`${data['model'][value]}`;
                                $(this).html(a_html)
                            }     
                        }
                    });
                });            
        }
        // Macroeconomicparameters
        $('body').on("submit",".model-macroeconomicparameters-edit",function(e){
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
                beforeSubmit:  $('#submit_macroeconomicparameters').attr('disabled', 'disabled'),
                success: function(data){
                    if (data) {
                        if (data['error']=== false || data['model']) {
                            //--update changes
                            updatemacroeconomicparametersTable(data);
                            checkReadyModel();
                        }							
                       $('#submit_macroeconomicparameters').removeAttr('disabled')
                       $('#modal_add_model_macroeconomicparameters').modal('hide');
                       $('.close-modal').click() 
                    }
                },
                error: function (exception) {
                    console.log(exception);
                    $('#submit_macroeconomicparameters').removeAttr('disabled')
                }
            })
            return false;
        })

        $('body').on("submit",".model-macroeconomicparameters-add",function(e){
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
                beforeSubmit:  $('#submit_macroeconomicparameters').attr('disabled', 'disabled'),
                success: function(data){
                    if (data) {
                        if (data['error']=== false || data['model']) {
                            //--update changes
                            addmacroeconomicparametersTable(data);
                            checkReadyModel();
                        }							
                       $('#submit_macroeconomicparameters').removeAttr('disabled')
                       $('#modal_add_model_macroeconomicparameters').modal('hide');
                       $('.close-modal').click() 
                    }
                },
                error: function (exception) {
                    console.log(exception);
                    $('#submit_macroeconomicparameters').removeAttr('disabled')
                }
            })
            return false;
        })
        function addmacroeconomicparametersTable(data){
            console.log('addmacroeconomicparametersTable')
            var model_or_data= ''
            if (data['data']){
                model_or_data='data'
            } else if (data['model']){
                model_or_data='model'
            } 
            $("#macroeconomicparameters_section").children(".view-section").each(function() {
                var attr = $(this).attr("name");
                console.log('before updating',attr )
                if (attr == "my_macroeconomicparameters_section") {                           
                    html_lead=`<table id="macroeconomicparametersTable" class="table table-striped" >
                        <thead>
                        </thead>
                        <tbody id="macroeconomicparameters-table-tbody">`
                    const obj = {
                        discount_rate_equity: 'discount_rate_equity',
                        domestic_inflation_rate: 'domestic_inflation_rate',
                        us_inflation_rate: 'us_inflation_rate',
                        exchange_rate: 'exchange_rate',
                        dividend_payout_ratio: 'dividend_payout_ratio',
                        num_of_shares: 'num_of_shares',
                        investment_costs_over_run_factor: 'investment_costs_over_run_factor',
                        
                    };

                    
                    html_body =''
                    $.each(obj, function(key, value) {                                
                        x=  `<tr id="macroeconomicparameters-${key}" >
                            <th scope="row">${value}</th>
                            <td class="macroeconomicparametersAction macroeconomicparametersData" name="${key}" >${data[model_or_data][key]}</td>                                                    
                            </tr>`
                        html_body = html_body + x
                    });
                    html_trail= `</tbody>
                        </table>
                        </div>
                        <a class="model-edit show-form-update" href="#" data-url="/update_model_macro_economic_parameters_ajax/${data[model_or_data].id}/" 
                        data-target="#modal-edit-product-div" data-toggle="tooltip" data-placement="bottom" 
                        title='Edit Taxes'><i  class="fas fa-edit"></i>
                      </a>` ;
                    
                    a_html =html_lead + html_body + html_trail
                    $(this).html(a_html)
                    //prepare for updating
                    console.log('model_id', data[model_or_data].model_id)
                    url=`/update_model_macro_economic_parameters_ajax/${data[model_or_data].id}/`
                    $("#form-macroeconomicparameters").attr( "data-url",  url)
                    $("#macroeconomicparameters_label").html(`Edit macroeconomicparameters Parameters: ${truncChar(data[model_or_data].model_name,15)}`)
                    
                    html_add_check= `<a class="nav-link active show" data-bs-toggle="tab" href="#tab-7">
                    <i class="bi bi-check-circle"></i> Macro Economic Parameters</a>`;
                    $("#macroeconomicparameters_tab").html(html_add_check)
            
                    
                    // change destination ajax form class
                    $("#form-macroeconomicparameters").attr( "class",  "model-macroeconomicparameters-edit")                           
                    $("#macroeconomicparameters_accordion_button").removeClass( "section-incomplete")
                    $("#macroeconomicparameters_accordion_button").addClass( "section-complete") 
                    
                    
                   
                
                }
            });                   
        }               
        function updatemacroeconomicparametersTable(data){
                const obj = {
                    discount_rate_equity: 'discount_rate_equity',
                    domestic_inflation_rate: 'domestic_inflation_rate',
                    us_inflation_rate: 'us_inflation_rate',
                    exchange_rate: 'exchange_rate',
                    dividend_payout_ratio: 'dividend_payout_ratio',
                    num_of_shares: 'num_of_shares',
                    investment_costs_over_run_factor: 'investment_costs_over_run_factor',
                };

             
                $.each(obj, function(key, value) {
                    console.log(value);
                    $("#macroeconomicparametersTable #macroeconomicparameters-"+ value).children(".macroeconomicparametersData").each(function() {
                        var attr = $(this).attr("name");
                        if (attr == value) {
                            if (data['data']){
                                a_html =`${data['data'][value]}`;
                                $(this).html(a_html)
                            }else if(data['model']){
                                a_html =`${data['model'][value]}`;
                                $(this).html(a_html)
                            }     
                        }
                    });
                });            
        }

        function truncChar(inpstr,length){
            var myTruncatedString = inpstr.substring(0,length);              
            if (inpstr.length > myTruncatedString.length){
              return myTruncatedString + "..."
            }
            return myTruncatedString
        } 
      
       
        

 })