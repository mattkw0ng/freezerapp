$(document).ready(function(){
  $('.single-freezer-view').slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    arrows: false,
    fade: true,
    asNavFor: '.slides'
  });
  $('.slides').slick({
    centerMode: true,
    centerPadding: '60px',
    slidesToShow: 3,
    prevArrow: '#prev-arrow',
    nextArrow: '#next-arrow',
    asNavFor: '.single-freezer-view',
    swipeToSlide: true,
    responsive: [
      {
        breakpoint: 768,
        settings: {
          arrows: false,
          centerMode: true,
          centerPadding: '40px',
          slidesToShow: 3
        }
      },
      {
        breakpoint: 480,
        settings: {
          arrows: false,
          centerMode: true,
          centerPadding: '40px',
          slidesToShow: 1
        }
      }
    ]
  });
});

function add_freezer(){
  window.location.href = '/add-freezer';
}