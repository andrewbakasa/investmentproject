/**
* Template Name: Mentor - v4.7.0
* Template URL: https://bootstrapmade.com/mentor-free-education-bootstrap-theme/
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/
(function() {
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim()
    if (all) {
      return [...document.querySelectorAll(el)]
    } else {
      return document.querySelector(el)
    }
  }

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    let selectEl = select(el, all)
    if (selectEl) {
      if (all) {
        selectEl.forEach(e => e.addEventListener(type, listener))
      } else {
        selectEl.addEventListener(type, listener)
      }
    }
  }

  /**
   * Easy on scroll event listener 
   */
  const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener)
  }

  /**
   * Back to top button
   */
  let backtotop = select('.back-to-top')
  if (backtotop) {
    const toggleBacktotop = () => {
      if (window.scrollY > 100) {
        backtotop.classList.add('active')
      } else {
        backtotop.classList.remove('active')
      }
    }
    window.addEventListener('load', toggleBacktotop)
    onscroll(document, toggleBacktotop)
  }

  /**
   * Mobile nav toggle
   */
  on('click', '.mobile-nav-toggle', function(e) {
    select('#navbar').classList.toggle('navbar-mobile')
    this.classList.toggle('bi-list')
    this.classList.toggle('bi-x')
  })

  /**
   * Mobile nav dropdowns activate
   */
  on('click', '.navbar .dropdown > a', function(e) {
    if (select('#navbar').classList.contains('navbar-mobile')) {
      e.preventDefault()
      this.nextElementSibling.classList.toggle('dropdown-active')
    }
  }, true)

  /**
   * Preloader
   */
  let preloader = select('#preloader');
  if (preloader) {
    window.addEventListener('load', () => {
      preloader.remove()
    });
  }

  /**
   * Testimonials slider
   */
  new Swiper('.testimonials-slider', {
    speed: 600,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false
    },
    slidesPerView: 'auto',
    pagination: {
      el: '.swiper-pagination',
      type: 'bullets',
      clickable: true
    },
    breakpoints: {
      320: {
        slidesPerView: 1,
        spaceBetween: 20
      },

      1200: {
        slidesPerView: 2,
        spaceBetween: 20
      }
    }
  });

  /**
   * Animation on scroll
   */
  window.addEventListener('load', () => {
    AOS.init({
      duration: 1000,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    })
  });

})()
// to remove message mailbox
$('.my_messages_li[mymessages_na]').each( function (){
  $(this).css(
      { "display":"none",
      }
  ).remove()          
})  
$('.my_messages_li[mymessages').each( function (){
  $(this).css({ "display":"block"})         
})
// to remove message mailbox
$('.my_messages2_li[mymessages2_na]').each( function (){
  $(this).css(
      { "display":"none",
      }
  ).remove()  
        
}) 

$('.my_messages2_li[mymessages2').each( function (){
  $(this).css({ "display":"block"})         
}) 

checkPosition_map_apartment()
//checkPosition_product_details()
$(window).resize(function() {
  checkPosition_map_apartment()
  //checkPosition_product_details()
  
 
 });

function checkPosition_map_apartment() {
    if ( window.matchMedia('(max-width: 767px)').matches)   {// mobile
      $("#setfull_map").css({'display': 'None'})
    }else{
      $("#setfull_map").css({'display': 'block'})
    }
    let isChecked = $('#setfull_map').is(':checked');
     // $('#setfull_map').prop("checked")
    if (isChecked){
      map_full_screen()
    }else {
      resize_match()
    }

    
}
function resize_match(){
  if ( window.matchMedia('(max-width: 767px)').matches)   {// mobile
    $(".apartment-handle").css({'display': 'None'})
    $(".footer-top").css({'display': 'None'})
  }else {
    $(".apartment-handle").css({'display': 'block'})
    $(".footer-top").css({'display': 'block'})
  }
  if ( window.matchMedia('(max-width: 991px)').matches)   {// mobile
     
      $(".apartment-handle").removeClass('col-md-8')
      $(".apartment-handle").removeClass('col-md-pull-4')
      
    
      $(".apartment-handle").removeClass('col-md-0')
      $(".apartment-handle").removeClass('col-md-pull-12')
      
      //Set 50:50
      $(".apartment-handle").addClass('col-md-6')
      $(".apartment-handle").addClass('col-md-pull-6')

      $(".map-handle").removeClass('col-md-4')
      $(".map-handle").removeClass('col-md-push-4')
      $(".map-handle").removeClass('col-md-12')
      $(".map-handle").removeClass('col-md-push-12') 

      //Set 50:50
      $(".map-handle").addClass('col-md-6')
      $(".map-handle").addClass('col-md-push-6') 
  } else {// wide screen
   
    wide_screen_standard()
  
  }
}
$('#setfull_map').change(function() {

	checkPosition_map_apartment()
});
function wide_screen_standard(){
 
  $(".apartment-handle").css({'display': 'block'})
  $(".apartment-handle").removeClass('col-md-6')
  $(".apartment-handle").removeClass('col-md-pull-6')

  $(".apartment-handle").removeClass('col-md-0')
  $(".apartment-handle").removeClass('col-md-pull-12')


  //set 80:40
  $(".apartment-handle").addClass('col-md-8')
  $(".apartment-handle").addClass('col-md-pull-4')

  $(".map-handle").removeClass('col-md-6')
  $(".map-handle").removeClass('col-md-push-6')
  $(".map-handle").removeClass('col-md-12')
  $(".map-handle").removeClass('col-md-push-12') 

  //
  $(".map-handle").addClass('col-md-4')
  $(".map-handle").addClass('col-md-push-4') 
  /* AFTER EFFECT */
  var width = $('#project_div').width()-$('.map').left; 
  var height = $('#project_div').height();
  console.log('left',-$('.map').left)
  if (height>600)
    height=600 
  //reduce height
  if (1.2*width<height)
      height=1.2*width
 
  console.log('project_width', $('#project_div').width(),'window-widht', $(window).width(),$(window).width()-$('#project_div').width())
  $(".map").css({'width':width ,'height':height})
  console.log('mapt_width', $('.map').width())
  $(window).trigger('resize');
}
function map_full_screen(){
      if ( window.matchMedia('(max-width: 767px)').matches)   {// mobile
        $(".footer-top").css({'display': 'None'})
      }else {
        $(".footer-top").css({'display': 'block'})
      }
     
 
      $(".apartment-handle").css({'display': 'None'})
      $(".apartment-handle").removeClass('col-md-6')
      $(".apartment-handle").removeClass('col-md-pull-6')
      $(".map-handle").removeClass('col-md-4')
      $(".map-handle").removeClass('col-md-push-4')

      //set 80:40
      $(".apartment-handle").addClass('col-md-0')
      $(".apartment-handle").addClass('col-md-pull-12')

      
      $(".map-handle").removeClass('col-md-6')
      $(".map-handle").removeClass('col-md-push-6')
      $(".map-handle").removeClass('col-md-4')
      $(".map-handle").removeClass('col-md-push-4')

      //
      $(".map-handle").addClass('col-md-12')
      $(".map-handle").addClass('col-md-push-12') 
      /* AFTER EFFECT */
      var width = $('#project_div').width()-$('.map').left; 
      var height = $('#project_div').height();
      console.log('left',-$('.map').left)
      if (height>600)
          height=600
      //reduce height
      if (1.2*width<height)
          height=1.2*width
      console.log('project_width', $('#project_div').width(),'window-width', $(window).width(),$(window).width()-$('#project_div').width())
 
      $(".map").css({'width':width ,'height':height})
      console.log('mapt_width', $('.map').width())
      $(window).trigger('resize');
}

