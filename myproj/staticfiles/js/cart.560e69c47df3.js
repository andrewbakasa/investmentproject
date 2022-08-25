//console.log('Hello World')

var updateButtons = document.getElementsByClassName('update-cart')

// for(i = 0; i < updateButtons.length; i++){
//     updateButtons[i].addEventListener('click', function(){
//         var productId = this.dataset.product
//         var action = this.dataset.action
//         console.log('productId: ', productId, 'action: ', action)

//         console.log('user: ', user)

//         if(user === 'AnonymousUser'){
//             addCookieItem(productId, action)
//         }else{
//             updateUserOrder(productId, action)
//         }
//     })
// }
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
function updateToProductTabel(product){
   
    $("#o_total_qnty").html(`<h5>Items: <strong>${numberWithCommas(product.o_total_qnty)}</strong></h5>`)
    $("#o_total_price").html(`<h5>Total: <strong>$${numberWithCommas(product.o_total_price)}</strong></h5>`)

    $("#cart-total").text(product.o_total_qnty)
    if (product.deleted){
        $("#cart-item-" + product.id).remove()
    }
    
    $("#cart-item-" + product.id).children().each(function() {
        //console.log('inside')
        var attr = $(this).attr("name");
        if (attr == "item") {
         // $(this).text(product.name);
        } else if (attr == "price") {
          //$(this).text(product.price);
        } else if (attr == "quantity") {
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
            
                if (response.data) {
                updateToProductTabel(response.data);
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
    //console.log('Not logged in.')

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