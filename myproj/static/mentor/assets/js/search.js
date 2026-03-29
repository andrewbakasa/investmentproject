$(document).ready(function(){

      function mobile_view(){
          
          var sbutton = $('#searchbutton');

          //console.log('First', sbutton[0] , sbutton.parent()[0])
          
          // remove it if not already removed
          if (sbutton.parents('nav#navbar').length){
              //remove it if in ul tag
              sbutton.remove()
              //append here
              sbutton.insertAfter("#navbar")
              // $('table').removeClass('table table-striped');
              //console.log('DESKTOP-MOBILE SHIFT')
          }else{
              //console.log('IN MOBILE VIEW')
          }

          



      }

      function desktop_view(){
          var sbutton = $('#searchbutton');
          var navbar_ul =$('#navbar-ul')
          
          //change only if search is in mobile// does not have parenr
          if (!(sbutton.parents('nav#navbar').length)){
             //remove it and append some
              sbutton.remove()
              //append in ul tag
              navbar_ul.append(sbutton)
              // $('table').addClass('table table-striped')
              //console.log('MOBILE-DESKTOP SHIFT')
          }else {
            //console.log('IN DESKTOP VIEW')
          }
         
         ;
      }
      checkPosition_product_details()
      $(window).resize(function() {
       // console.log('width',$(this).width()  )
       checkPosition_product_details()
          if ($(this).width() < 991) {
            mobile_view()
          } else {
            desktop_view()
          }
          //checkPosition() 
      });
    //does it on start
    checkPosition()

    
    function checkPosition() {
      //mobile
      
        if (
            (window.matchMedia('(max-width: 760px)').matches) || 
            ((window.matchMedia('min-device-width: 768px').matches) && (window.matchMedia('max-device-width: 1024px').matches)) 
            ) {
            mobile_view()
        } else {
            desktop_view() 
        }
    }

    function checkPosition2() {
        //mobile
        if (window.matchMedia('(max-width: 768px)').matches) {
          mobile_view()
        } else {
          desktop_view() 
        }
    }
  
   
    $('body').on("focus","#search",function(e){
      $(".search-box").addClass("border-searching");
      $(".search-icon").addClass("si-rotate");
    })

    
    $('body').on("blur","#search",function() {
      $(".search-box").removeClass("border-searching");
      $(".search-icon").removeClass("si-rotate");
    });
    

    $('body').on("keyup","#search",function() {
        if($(this).val().length > 0) {
          $(".go-icon").addClass("go-in");
        }
        else {
          $(".go-icon").removeClass("go-in");
        }
    });
    $('body').on("click",".go-icon",function() {
    //   $(".search-form").submit();
    // ajax
    
    });
   
    // For now I've settled for a hacky fix, forcing focus back onto the <input> element 700 milliseconds after a click:
    // . I guess this redraws the DOM and so causes anything in the DOM to lose focus. I stopped this from happening on resize - making it only happen on initial page load instead.
    // Android - html input loses focus when soft keyboard opens
   /*  $('body').on("click","#search",function(evt) {
       
        var focusClosure = (function(inputElem) {return function() {
          console.log(inputElem.focus());
        }}($(evt.target)));
        
        window.setTimeout(focusClosure, 700);
      
    }); */
});

function checkPosition_product_details() {
  if ( window.matchMedia('(max-width: 767px)').matches)   {// mobile
      $("#img-and-btn-wrapper").removeClass('col-md-4')
      $("#img-and-btn-wrapper").removeClass('col-md-pull-8')

      //Set 100
      $("#img-and-btn-wrapper").addClass('col-md-12')
      $("#img-and-btn-wrapper").addClass('col-sm-12')
      $("#img-and-btn-wrapper").addClass('col-xm-12')

      $("#product-details-description").removeClass('col-md-8')
      $("#product-details-description").removeClass('col-md-push-4')

      //Set 50:50
      $("#product-details-description").addClass('col-md-12') 
  } else {// wide screen
    $("#img-and-btn-wrapper").removeClass('col-md-12')
    $("#img-and-btn-wrapper").removeClass('col-sm-12')
    $("#img-and-btn-wrapper").removeClass('col-xm-12')


    //set 80:40
    $("#img-and-btn-wrapper").addClass('col-md-4')
    $("#img-and-btn-wrapper").addClass('col-md-pull-8')

    $("#product-details-description").removeClass('col-md-12')


    //
    $("#product-details-description").addClass('col-md-8')
    $("#product-details-description").addClass('col-md-push-4') 
  }
}