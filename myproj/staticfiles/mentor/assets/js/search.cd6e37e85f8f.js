$(document).ready(function(){

      function mobile_view(){
          var sbutton = $('#searchbutton');
          //remove it if in ul tag
          sbutton.remove()
          //append here
          sbutton.insertAfter("#navbar")
      }

      function desktop_view(){
          var sbutton = $('#searchbutton');
          var navbar_ul =$('#navbar-ul')
          //remove it and append some
          sbutton.remove()
          //append in ul tag
          navbar_ul.append(sbutton)
      }
      $(window).resize(function() {
          if ($(this).width() < 991) {
            mobile_view()
          } else {
            desktop_view()
          }
      });
    //does it on start
    checkPosition()

    function checkPosition() {
        //mobile
        if (window.matchMedia('(max-width: 991px)').matches) {
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
});