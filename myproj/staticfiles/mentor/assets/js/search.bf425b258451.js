$(document).ready(function(){

      function mobile_view(){
          var sbutton = $('#searchbutton');
          //remove it if in ul tag
          sbutton.remove()
          //append here
          sbutton.insertAfter("#navbar")
          // $('table').removeClass('table table-striped');



      }

      function desktop_view(){
          var sbutton = $('#searchbutton');
          var navbar_ul =$('#navbar-ul')
          //remove it and append some
          sbutton.remove()
          //append in ul tag
          navbar_ul.append(sbutton)
          // $('table').addClass('table table-striped');
      }
      $(window).resize(function() {
        console.log('width',$(this).width()  )
          if ($(this).width() < 744) {
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
    $('input').click(function () {
      var val = $(this).val();
      // console.log('>>>',val)
      if (val == "") {
          // console.log('>>> EMPY VAL')
          this.select();
      }
  });
   
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
    $('body').on("click","#search",function(evt) {
       
        var focusClosure = (function(inputElem) {return function() {
          console.log(inputElem.focus());
        }}($(evt.target)));
        
        window.setTimeout(focusClosure, 700);
      
      });
});