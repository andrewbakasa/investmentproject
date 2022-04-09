  
  $(document).ready(function(){                       
        function updateTable(item){
            //after edit update the table
            $("#modelTable #" + item.id).children(".modelData").each(function() {
                var attr = $(this).attr("name");
                if (attr == "model_type") {
                $(this).text(item.model_type);
                } else if (attr == "name") {
                $(this).text(item.name);
                } else if (attr == "currency") {
                $(this).text(item.currency);
                } else if (attr == "simulation_run") {
                var html =''
                if (item.simulation_run){
                    html = `<input type="checkbox" checked disabled> `;
                }else {
                    html = `<input type="checkbox"  disabled> `;
                }            
                
                $(this).html(html);
                } else if (attr == "simulation_iterations")  {
                $(this).text(item.simulation_iterations);
                } else if (attr == "npv_bin_size")  {
                $(this).text(item.npv_bin_size);
                } 
            });
        }

        function updatePaging(pages){ 
            // dynamincally add pages...
            
            var page_section = $('#page_section')
            if (page_section[0]==undefined) {
                // console.log('...First Model: Empty Model Table')
                $('#models_placeholder').html('');
                a_html = 	usermodelhtml() ;                
                $('#models_placeholder').append(a_html);

            }   
            $('.pagination').html('');
            for (let i = 1; i < pages+1; i++) {
                a_html = 	`<a class='a_page_nav' style="margin-left: 5px; " href="${i}">${i}</a>` ;
                $('.pagination').append(a_html)
            }
        }
        function usermodelhtml(){
            a_html = 	`<div class="table-responsive">
                            <table class="table table-striped">
                                <thead >
                                    <th style="width: 2%">#</th>  
                                    <th style="width: 8%">Category</th>
                                    <th style="width: 15%">Title</th>
                                    <th style="width: 5%">Currency</th>              
                                    <th style="width: 5%">Simulate</th>
                                    <th style="width: 5%">Runs</th>
                                    <th style="width: 6%">Bin</th>
                                    <th style="width: 39%">Created on</th>
                                    <th style="width: 5%">Ready</th>
                                    <th  style="width: 8%" class="text-right">Actions</th>
                                </thead>
                                <tbody id="modelTable">
                                
                                </tbody>
                            </table>
                        </div>
                        <div class="pagination">
                            
                        </div>` ;
                return a_html
        }
        
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

        $('#confirmdelete').on('show.bs.modal', function(e) {
                var name = $(e.relatedTarget).data('object-name');
                var url = $(e.relatedTarget).data('delete-url');
                var model_id = $(e.relatedTarget).data('model-id');
                $('#confirmdelete .modal-body').text("Are you sure you want to delete " + name + "?");
                //$('#confirmdelete .modal-footer a').attr('href', url);
                $('#confirmdelete .modal-footer input').attr('data-url', url);
                $('#confirmdelete .modal-footer input').attr('model-id', model_id);
            });
    
        $('body').on('click', '.delete-button', function (e) {
            e.preventDefault();
            var tr_id =$('#delete-button').attr('model-id')
            row = $('#'+ tr_id.trim());
            var formData = {
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            };
            $.ajax({
                type: 'POST',      
                url:   $('#delete-button').attr('data-url'), 
                encode: true,
                contentType: 'application/x-www-form-urlencoded',
                crossDomain: false,
                dataType: 'json',
                data: formData,     // our data object
                success: function (data) {
                    
                    if (data.data.total_pages){
                        //update paging numbering if need be
                        updatePaging(data.data.total_pages)
                    }
                    row.fadeOut(1000, function () {
                        //remove the row deleted
                        $(this).remove();
                        // if deleted page make the page disappear, point to prev page
                        //page-1
                        if (data.data.total_pages< data.data.deleted_page){                     
                            var index= parseInt(data.data.total_pages)-1
                            window.setTimeout(function() {
                                $(".a_page_nav:eq(" +  index  +")").trigger('click');
                            }, 1000);
                        }else{
                            // if item on the current page get to zero
                            // point to page-1
                            var total = $('#modelTable').children().length
                            //console.log('total items in dom>>>',total)
                            if (total == 0){
                                //refresh the current pages
                                var index= parseInt(data.data.deleted_page)-1
                                console.log('Empy page.. load page behind this current page', index)
                                $(".a_page_nav:eq(" +  index  +")").trigger('click');
                            }

                        }
                       
                    });
                    // if deleting page one and there are more pages behind.... push al those pages
                   
                    $('#confirmdelete').modal('hide');
                    $('.close-modal').click() 
                },
                error: function (exception) {
                    alert('Exeption:' + exception);
                }
            });
        });
        // search all records.............
        $("#search_input").on("keyup", function() {
            var value = $(this).val().toLowerCase();
            $("#modelTable tr").filter(function() {
                $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
            });
        });
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
        //EDIT NEW MODEL
        $('body').on("submit",".model-form-edit",function(e){
            e.preventDefault();
            var data = new FormData(this);
            var formData
            var form = $(this);
           
            var url=form.attr('data-url')
            $.ajax({
                url: form.attr('data-url'),
                data : data,
                type: form.attr('method'),
                dataType: 'json',
                processData:false,
                contentType: false,
                success: function(data){
                    if(data.model){
                        console.log('updating')
                        updateTable(data.model);
                        //hide the form after editing
                        $('#modal-usermodel').modal('hide');
                        $('.close-modal').click() 
                    } else {
                        $('#public_toggle_form-errors').html('');
                        if (data.error) {
                            var form_vars=['__all__','name','model_type', 'currency', 'simulation_iterations',  'simulation_run', 'npv_bin_size']//,
                    
                            for (let p=0; p < form_vars.length; p++ ){
                                let name_var = form_vars[p]
                                if (data.error[name_var]){
                                a_html = 	`<div class='alert alert-danger alert dismissable'>
                                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                                    <span aria-hidden="true">&times;</span></button>${data['error'][name_var][0]}
                                </div> ` ;
                                $('#public_toggle_form-errors').append(a_html)
                                
                                }
                            }
                            $('#public_toggle_form-errors').slideUp(50).fadeIn();
                            window.setTimeout(function() {
                                $("#public_toggle_form-errors").fadeIn().slideUp(500, function(){
                                    $("#public_toggle_form-errors").html('');
                                });
                            }, 4000);
                        //-----------------------
                        } else  {
                            // Data locked:  No edit allowed
                            $('#public_toggle_form-errors').html('');
                            a_html = 	`<div class='alert alert-danger alert dismissable'>
                            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                            <span aria-hidden="true">&times;</span></button>${data['locked']}
                            </div> ` ;
                            $('#public_toggle_form-errors').append(a_html)
                            $('#public_toggle_form-errors').slideUp(50).fadeIn();                           

                            window.setTimeout(function() {
                                $("#public_toggle_form-errors").fadeIn().slideUp(500, function(){
                                    $("#public_toggle_form-errors").html('');
                                });
                                }, 4000);
                        } 
                    //LAST ELSE--------------------------------------                
                    }
                //END SUCCESS
                }
            // END AJAX
            })
            return false;
        })
        
        //ADD MODEL FORM
        $('body').on("submit",".model-form-add",function(e){
            e.preventDefault();            
            var data = new FormData(this);
            var formData
            var form = $(this);
        
            $.ajax({
                url: form.attr('data-url'),
                //data: form.serialize(),
                data : data,
                type: form.attr('method'),
                dataType: 'json',
                processData:false,
                contentType: false,
                success: function(data){ 
                    if(data.model){ 
                        //---------HIDE ADD(+)----------------------              
                        $('#modal_add_new_model').modal('hide');
                        $('.close-modal').click() 
                        //update paging
                        if (data.total_pages){
                            updatePaging(data.total_pages)
                        }
                        //click first instance of page_class to show newly addition
                        $('.a_page_nav:first-child').trigger('click');
                        //----------------------------------
                    } else {
                        // ADDITION NOT SUCCESSFUL
                        $('#public_toggle_form-errors').html('');
                        if (data['error']) {
                            var form_vars=['__all__','name','model_type', 'currency','user']
                            for (let p=0; p < form_vars.length; p++ ){
                                let name_var = form_vars[p]
                                if (data['error'][name_var]){
                                    a_html = 	`<div class='alert alert-danger alert dismissable'>
                                        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                                        <span aria-hidden="true">&times;</span></button>${data['error'][name_var][0]}
                                    </div> ` ;
                                    $('#public_toggle_form-errors').append(a_html)
                                }
                            }
                            $('#public_toggle_form-errors').slideUp(50).fadeIn();
                            window.setTimeout(function() {
                                $("#public_toggle_form-errors").fadeIn().slideUp(500, function(){
                                    $("#public_toggle_form-errors").html('');
                                });
                                }, 4000);
                            //-----------------------
                        } else  {
                            // Data locked:  No edit allowed
                            $('#public_toggle_form-errors').html('');
                            a_html = 	`<div class='alert alert-danger alert dismissable'>
                            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                            <span aria-hidden="true">&times;</span></button>${data['locked']}
                            </div> ` ;
                            $('#public_toggle_form-errors').append(a_html)
                            $('#public_toggle_form-errors').slideUp(50).fadeIn();

                            window.setTimeout(function() {
                                $("#public_toggle_form-errors").fadeIn().slideUp(500, function(){
                                    $("#public_toggle_form-errors").html('');
                                });
                                }, 4000);

                        } 
                    //LAST ELSE--------------------------------------                
                    }
                //END SUCCESS
                }
            // END AJAX
            })
            return false;
        })

        $('body').on('click', '.a_page_nav', function (event) {
            // preventing default actions
            event.preventDefault();
            var page_no = $(this).attr('href');
            // ajax call
            $.ajax({
                type: "POST",
                // define url name
                url: display_models_ajax_url, 
                data : {    
                    page_no : page_no, 
                    csrfmiddlewaretoken: csrftoken,
                },
                // handle a successful response
                success: function (response) {
                    $('#modelTable').html('')
                    var per_page=4
                    if (response.data.per_page){
                        per_page=response.data.per_page
                    }
                    var base_counter =(parseInt(page_no)-1)*per_page
                    var counter=base_counter
                    $.each(response.data.results, function(i, val) {
                        var simulation_checked=''
                        if (val.simulation_run) {
                            simulation_checked='checked'
                        }
                        var design_complete_checked=''
                        if (val.design_complete) {
                            design_complete_checked='checked'
                        }
                        var js_date_created = new Date(val.date_created)
                        //append to post
                       
                        counter=  counter+1
                       
                        a_html=`
                         <tr id="${val.id}" >
                            <td class="modelModelType modelData" > ${counter}</td>
                            <td class="modelModelType modelData" name="model_type" >${val.model_type}</td>
                            <td class="modelModelType modelData" name="name" >${val.name}</td>               
                            <td class="modelModelType modelData" name="currency" >${val.currency}</td>
                            <td class="modelModelType modelData" name="simulation_run" >
                                <input type="checkbox" ${simulation_checked} disabled> </td>
                            <td class="modelModelType modelData" name="simulation_iterations" >${val.simulation_iterations}</td>
                            <td class="modelModelType modelData" name="npv_bin_size" >${val.npv_bin_size}</td>
                            <td class="modelModelType modelData" name="date_created" >${js_date_created}</td>
                            
                            <td class="modelModelType modelData" name="design_complete" >
                            <input type="checkbox" ${design_complete_checked} disabled> </td>
                            <td class="text-right modelAction modelData" name="action">
                                <a href="/select_model/${val.id}/"
                                    style="color:inherit" data-toggle="tooltip" data-placement="bottom" 
                                    title='View Model'><i class="fa fa-eye"></i>
                                </a>
                                <a class="model-edit show-form-update" href="#" data-url="/update_model/${val.id}/" 
                                    data-target="#modal-edit-product-div" style="color:inherit" data-toggle="tooltip" data-placement="bottom" 
                                    title='Edit Model'><i class="fa fa-edit"></i>
                                </a>
                                <a href="#"  data-toggle="modal" data-target="#confirmdelete" 
                                    data-object-name="${val.name}"  data-model-id="${val.id}" 
                                    data-delete-url="/delete_bussiness_model_ajax/${val.id}/${page_no}/"  style="color: red" data-toggle="tooltip" data-placement="bottom" 
                                    title='Delete' > <i class="fa fa-trash "></i> 
                                </a>
                            </td>
                        </tr>` ;
                        // add each model on every line
                        $('#modelTable').append(a_html)
                    });
                    },
                    error: function () {
                        alert('Error Occured');
                    }
            }); 
        });    
  

     });

  
     