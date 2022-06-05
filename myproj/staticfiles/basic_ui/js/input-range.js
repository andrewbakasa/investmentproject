


function numberWithCommas(x) {
    var parts = x.toString().split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return parts.join(".");
}
$('body').on("change",".change-positivenumber",function(e){
    var item_id=$(this).attr('id')    
    validate_positivenumber(item_id)     
})



function validate_positivenumber(item_id){
    var val = parseFloat($('#'+ item_id).val())
    var allowed_range =Math.max(val,0)
    //clip range
    $('#'+ item_id).val(allowed_range)
   
}
function roundTo(value, places){
    var power = Math.pow(10, places);
    return Math.round(value * power) / power;
}


$('body').on("change",".change-positiveinteger",function(e){
    var item_id=$(this).attr('id')    
    validate_positiveinteger(item_id)     
})

function validate_positiveinteger(item_id){
    var val = parseInt($('#'+ item_id).val())
    var allowed_range =Math.max(val,0)
    //clip range
    $('#'+ item_id).val(allowed_range)
   
}


$('body').on("change",".change-percent",function(e){
    var item_id=$(this).attr('id')    
    validate_zero_to_hundred_percent(item_id)     
})

function validate_zero_to_hundred_percent(item_id){
    var val = parseFloat($('#'+ item_id).val())
    var allowed_range =Math.max(Math.min(val,1),0)
    //clip range
    $('#'+ item_id).val(allowed_range)
   
}

$('body').on("change",".change-financing",function(e){
    var item_id=$(this).attr('id')

    if (item_id == 'id_equity'){
        validate_senior_debt_from_equity_change()
    } 
    if (item_id == 'id_senior_debt'){
        validate_equity_from_senior_debt_change()
    } 
   
   
    
})



function validate_senior_debt_from_equity_change(){
    var equity = parseFloat($('#id_equity').val())
    var allowed_equity =Math.max(Math.min(parseFloat($('#id_equity').val()),1),0)

    var senior_debt = Math.max(Math.min(parseFloat($('#id_senior_debt').val()),1),0)
    var valid_senior_debt= roundTo(1.0 - allowed_equity,2)
    
    if (senior_debt !== valid_senior_debt){
        // pull base alogn construction start
        $('#id_senior_debt').val(valid_senior_debt)
    }

    if (equity !== allowed_equity){
        // pull base alogn construction start
        $('#id_equity').val(allowed_equity)
    }
}

function validate_equity_from_senior_debt_change(){
    
    var senior_debt = parseFloat($('#id_senior_debt').val())
    var allowed_senoir_debt =Math.max(Math.min(parseFloat($('#id_senior_debt').val()),1),0)
    
    var equity = Math.max(Math.min(parseFloat($('#id_equity').val()),1),0)  
    var valid_equity= roundTo(1.0 - allowed_senoir_debt,2)
    
    
    if (equity !== valid_equity){
        // pull base alogn construction start
        $('#id_equity').val(valid_equity)
    }

    if (senior_debt !== allowed_senoir_debt){
        // pull base alogn construction start
        $('#id_senior_debt').val(allowed_senoir_debt)
    }
}
function timing_assumption_module(){
    validate_base_period_from_construction_start_change()
    validate_construction_start_from_base_period_change()
    validate_construction()
    validate_construction_start()
    validate_operations() 
    validate_operation_start()
    validate_non_negative_construction_period()
    validate_operations2() 
       
}



$('body').on("change",".change-input",function(e){
    var item_id=$(this).attr('id')

    if (item_id == 'id_construction_start_year'){
        validate_base_period_from_construction_start_change()
    } 
    if (item_id == 'id_base_period'){
        validate_construction_start_from_base_period_change()
    } 
    if (item_id == 'id_construction_start_year' || 
            item_id == 'id_construction_len' ){
        validate_construction()
    }
   
    if (item_id == 'id_construction_year_end'){
        validate_construction_start()
    }

    
    if (item_id == 'id_operation_start_year' || 
            item_id == 'id_operation_duration' ){
            validate_operations() 
            validate_operation_start() 
    }

    if (item_id == 'id_construction_len'|| item_id == 'id_operation_duration'){
        validate_non_negative_val(item_id,0)
    }
    
    
    

    if (item_id == 'id_construction_len'){
        validate_non_negative_construction_period()
    } 

    if (item_id == 'id_operation_end'){
        validate_operations2()  
    }
    
})
function validate_non_negative_val(elem_id,lb){
    var con_len = parseInt($("#" + elem_id).val())
   
    if (con_len < lb){
        $("#" + elem_id).val(lb)
    }
}

function validate_base_period_from_construction_start_change(){
    console.log("1")
    var base_period = parseInt($('#id_base_period').val())
    var construction_start = parseInt($('#id_construction_start_year').val())
    
    if (construction_start < base_period){
        // pull base alogn construction start
        $('#id_base_period').val(construction_start)
    }
}

function validate_construction_start_from_base_period_change(){
    console.log("2")
    var base_period = parseInt($('#id_base_period').val())
    var construction_start = parseInt($('#id_construction_start_year').val())
   
    if (base_period > construction_start){
        // pull construct start if behind
        $('#id_construction_start_year').val(base_period) 
    }
}
function validate_non_negative_construction_period(){
    console.log('7')
    var con_len = parseInt($('#id_construction_len').val())
   
    if (con_len < 0){
        $('#id_construction_len').val(0)
    }
}

function validate_construction(){
    console.log('--validate_construction: 3')
    var con_start = $('#id_construction_start_year').val()
    var con_len = $('#id_construction_len').val()
    var con_end = $('#id_construction_year_end').val()
    
    //if (con_start.length != 0)
    //console.log(con_start,con_len,con_end)
    
    var valid_con_end= parseInt(get_val(con_start)) + parseInt(get_val(con_len))- parseInt(1)
    if (valid_con_end !== con_end){
        $('#id_construction_year_end').val(valid_con_end)
    }
}

function validate_construction_start(){
    console.log('--validate_construction start 4 ')
    var con_start = $('#id_construction_start_year').val()
    var con_len = $('#id_construction_len').val()
    var con_end = $('#id_construction_year_end').val()
   
    var valid_con_start= parseInt(get_val(con_end)) - parseInt(get_val(con_len))+ parseInt(1)
    if (valid_con_start !== con_start){
        $('#id_construction_start_year').val(valid_con_start)
    }
}
function get_val (variable){
    if ($.trim(variable) != '' || variable != 'undefined' || variable != null ){
        return $.trim(variable)
    } else {
        return 0
    }
}


function validate_operation_start(){
    console.log('6')
    var op_start =parseInt($('#id_operation_start_year').val())
    var base_period = parseInt($('#id_base_period').val())
    console.log(op_start,base_period, base_period > op_start)
    if (base_period > op_start){
        $('#id_operation_start_year').val(base_period)
    }
}

function validate_operations(){
    console.log('--validate_operations 5')
    var op_start = $('#id_operation_start_year').val()
    var op_dur = $('#id_operation_duration').val()
    var op_end = $('#id_operation_end').val()
    var valid_op_end= parseInt(get_val(op_start)) + parseInt(get_val(op_dur))- parseInt(1)+  parseInt(1)//additional year for shuttdown
    if (valid_op_end !== op_end){
        $('#id_operation_end').val(valid_op_end)
    }
}
function validate_operations2(){
    console.log('--validate_operations2: 8')
    var op_start = $('#id_operation_start_year').val()
    var op_dur = $('#id_operation_duration').val()
    var op_end = $('#id_operation_end').val()
    var valid_op_duration= parseInt(get_val(op_end)) - parseInt(get_val(op_start))- parseInt(1)+ parseInt(1)//additional year for shuttdown
    if (valid_op_duration !== op_dur){
        $('#id_operation_duration').val(valid_op_duration)
    }
}



// $('#modal-usermodel').on('shown.bs.modal', function(e) {
//     console.log('loaded modal')
//     // not working.... search  when modal is ready
//     //timing_assumption_module()
// });

$(document).on('shown.bs.modal','.modal',function(e){
    var form_id= $(this).find('form').attr('id')

    if(form_id ==='form-timing-assumptions'){
        
        timing_assumption_module()
    }else {
        //console.log('3.' , form_id)   
    }
   
   
})



