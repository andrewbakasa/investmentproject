
var update_setTimeOut=null;
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
function numberWithCommas(x) {
    var parts = x.toString().split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return parts.join(".");
    }
function updateToProductTabel(product,action){
   
    $("#o_total_qnty").html(`<h5>Items: <strong>${numberWithCommas(product.o_total_qnty)}</strong></h5>`)
    $("#o_total_price").html(`<h5>Total: <strong>$${numberWithCommas(product.o_total_price)}</strong></h5>`)

    $("#cart-total").text(product.o_total_qnty)
    $("#span-cart-total").text(product.o_total_qnty)
    if (product.o_total_qnty != 0){
        $("#span-cart-total").css({'display' : 'block'})

    }else {
        $("#span-cart-total").css({'display' : 'none'}) 
    }
   
    
    if (product.deleted){
        //$("#cart-item-" + product.id).remove()
        $("#t-tbody").children("."+ product.id).remove()
    }

    
    if  (product.quantity == 1 && action =="add" ) {
        //console.log("First Time ADDITION", product.quantity,action)
        var target = $("#div-" + product.id).children('.project-item')
        if (target.length==0)
            target = $("#img-and-btn-wrapper") 
            
        target.each( function(){
            if ($(this)[0].hasAttribute('mycart_na')){
                $(this).attr('mycart','');
                $(this).removeAttr('mycart_na')
                $(this).addClass('engagement') 
            }

            var target2 = $(this).find('.myspan')
            target2.removeAttr('mycart_na')
            target2.addClass('advanced2')

            target2.css(
                { "display":"block",
                // "title":"", 
                }
            )

            target2.fadeIn(600, function(){
                target2.text(`${product.quantity}`)
            });
            //clear previous time 
            if (update_setTimeOut){
                clearTimeout(update_setTimeOut);
                update_setTimeOut = null;
            } 
            update_setTimeOut=window.setTimeout(function() {
                target2.fadeIn(500, function(){
                    target2.text(`CartItem`)
                });
            }, 1000);
           

        })
       
    } else if ( action =="add" ) {//product.quantity == 1 &&
        //console.log("ADDITION", product.quantity,action)
        var target = $("#div-" + product.id).children('.project-item')
        if (target.length==0)
            target = $("#img-and-btn-wrapper") 
            
        target.each( function(){
           
            var target2 = $(this).find('.myspan')
            target2.fadeIn(600, function(){
                target2.text(`${product.quantity}`)
            });
           

            //clear previous time 
            if (update_setTimeOut){
                //console.log('Clearing Time Out')
                clearTimeout(update_setTimeOut);
                update_setTimeOut = null;
            }
            update_setTimeOut=window.setTimeout(function() {
                target2.fadeIn(500, function(){
                    target2.text(`CartItem`)
                });
            }, 1000);
           

        })
       
    

    }else if (action =="remove_from_cart") {

        //console.log(`removing CartItem ${product.id}  from CART`)
        var target = $("#div-" + product.id).children('.project-item')
        if (target.length==0)
            target = $("#img-and-btn-wrapper") 
            
        target.each( function(){
            
            if ($(this)[0].hasAttribute('mycart')){
                $(this).attr('mycart_na','');
                $(this).removeAttr('mycart')
                $(this).removeClass('engagement') 
            }
           
            var target2 = $(this).find('.myspan')
            target2.removeAttr('mycart_na')
            target2.addClass('advanced2')

            target2.css(
                { "display":"none",
                // "title":"", 
                }
            )
        })
    }

 
    $("#t-tbody").children("."+ product.id).children().each(function() {
        console.log('inside', $(this))
        var attr = $(this).attr("name");
        if (attr == "item") {
         // $(this).text(product.name);
        } else if (attr == "price") {
          //$(this).text(product.price);
        } else if (attr == "quantity") {
            console.log("2:Qnty : Action", product.quantity,action)
          $(this).find("p").html(`${numberWithCommas(product.quantity)}`);
        } else if (attr == "total") {
          $(this).html(`$${numberWithCommas(product.total)}`);
        }
      });
}
$('body').on("click",".update-cart",function(e){
    e.preventDefault();
    var url = '/e/update_item_ajax/'
    var productId = this.dataset.product
    var action = this.dataset.action
    
    if(user === 'AnonymousUser'){
        addCookieItem(productId, action)
    } 
    $.ajax({
        url: url,
        //data: form.serialize(),
        data : {    
        productId : productId, 
        action : action,
        csrfmiddlewaretoken: csrftoken,
    },
        type: "POST",
        success: function(response){
        if(response.data){
            //console.log("output", response.data)
            
                $('.close-modal').click()
                if (response.data) {
                updateToProductTabel(response.data, action);
                flip_cart_display()
                }
                //$('#modal-product').modal('hide');
        } else {
            // $('#modal-product .modal-content').html(data.html_form)
        }
        }
    })
   
    return false;
})
function flip_cart_display (){
    if ($('#cart-total').html() >0){
        $('#cart-total').css({ "display":"block"})
        }else {
        $('#cart-total').css({ "display":"none"})
    }     
}
function addCookieItem(productId, action){
    if(action == 'add'){
        // if the item with the product id is not in cart
        // add it to cart
        if(cart[productId] == undefined){
            cart[productId] = {'quantity': 1}
        }else{
            cart[productId]['quantity'] += 1
        }
    }else if(action == 'remove'){
        cart[productId]['quantity'] -= 1

        if(cart[productId]['quantity'] <= 0){
            delete cart[productId]
        }
    } else if(action == 'remove_from_cart'){
        cart[productId]['quantity'] = 0

        if(cart[productId]['quantity'] <= 0){
            delete cart[productId]
        }   

    }

    //console.log('Cart: ', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    //location.reload()
}

function updateUserOrder(productId, action){
    //console.log('User is authenticated. Sending data...')

    var url = '/e/update_item/'
    //console.log('...', url)
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body: JSON.stringify({'productId': productId, 'action': action})
    })

    .then((response) => {
        return response.json()
    })

    .then((data) => {
        //console.log('data: ', data)
        //location.reload()
    })
}