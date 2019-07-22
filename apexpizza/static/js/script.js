$('.hero-slider').slick({
    slidesToShow: 1,
    nextArrow: '<i class="hero-slider-next fa fa-angle-right"></i>',
    prevArrow: '<i class="hero-slider-prev fa fa-angle-left"></i>',
    infinite: true,
    speed: 500,
    fade: true,
    cssEase: 'linear',
    dots: true,
});

$('.sets-slider').slick({
    doots: false,
    infinite: true,
    centerMode: true,
    slidesToShow: 3,
    slidesToScroll: 1,
    nextArrow: '<i class="sets-slider-next fa fa-angle-right"></i>',
    prevArrow: '<i class="sets-slider-prev fa fa-angle-left"></i>',
    // autoplay: true,
    // autoplaySpeed: 2000,
    responsive: [{
        breakpoint: 768,
        settings: {
            slidesToShow: 1,
        }
    }]
})


$('.pizza-comp-option').click(function () {
    $(this).toggleClass('delete');
});

$(window).scroll(function () {
    var windowTop = $(document).scrollTop();
    var header = $('.header');
    var body = $('body');
    if (windowTop > 70) {
        header.addClass('sticky');
        body.addClass('sticky');
    } else {
        header.removeClass('sticky');
        body.css('margin-top', '125');
        body.removeClass('sticky');
    }
})

$(window).scroll(function () {
    var windowTop = $(document).scrollTop();
    var logo = $('.header-sticky-logo')
    if (windowTop > 50) {
        logo.addClass('display');
    } else {
        logo.removeClass('display');
    }
})

$(".header-menu ul").on("click", "a", function (event) {
    // event.preventDefault();
    var id = $(this).attr('href');
    var top = $(id).offset().top;

    $('body,html').animate({
        scrollTop: top
    }, 1500);
});

$('.amount-remove').on('click', function (e) {
    e.preventDefault();
    var $this = $(this);
    var $input = $this.closest('div').find('input');
    var value = parseInt($input.val());

    if (value > 1) {
        value = value - 1;
    } else {
        value = 0;
    }

    $input.val(value);

});

$('.amount-add').on('click', function (e) {
    e.preventDefault();
    var $this = $(this);
    var $input = $this.closest('div').find('input');
    var value = parseInt($input.val());

    if (value < 100) {
        value = value + 1;
    } else {
        value = 100;
    }

    $input.val(value);
});

$('.header-cart-toggler').click(function () {
    $(this).toggleClass('rotate');
    $('.header-cart-products').toggleClass('visible');
    $('.header-cart').toggleClass('width');
})

$('.header-toggler').click(function () {
    $(this).toggleClass('active');
    $('.header-mobile-menu').toggleClass('visible');
    $('body').toggleClass('overflow');
});

$('.header-mobile-menu ul li a').click(function () {
    $('.header-toggler').toggleClass('active');
    $('.header-mobile-menu').toggleClass('visible');
    $('body').toggleClass('overflow');
});

$(".header-mobile-menu ul").on("click", "a", function (event) {
    event.preventDefault();
    var id = $(this).attr('href');
    var top = $(id).offset().top;

    $('body,html').animate({
        scrollTop: top
    }, 1500);
});

// This button will increment the value
$('.qtyplus').click(function (e) {
    // Stop acting like a button
    e.preventDefault();
    // Get the field name
    fieldName = $(this).attr('field');
    // Get its current value
    var currentVal = parseInt($('input[name=' + fieldName + ']').val());
    // If is not undefined
    if (!isNaN(currentVal)) {
        // Increment
        $('input[name=' + fieldName + ']').val(currentVal + 1);
    } else {
        // Otherwise put a 0 there
        $('input[name=' + fieldName + ']').val(0);
    }
});
// This button will decrement the value till 0
$(".qtyminus").click(function (e) {
    // Stop acting like a button
    e.preventDefault();
    // Get the field name
    fieldName = $(this).attr('field');
    // Get its current value
    var currentVal = parseInt($('input[name=' + fieldName + ']').val());
    // If it isn't undefined or its greater than 0
    if (!isNaN(currentVal) && currentVal > 0) {
        // Decrement one
        $('input[name=' + fieldName + ']').val(currentVal - 1);
    } else {
        // Otherwise put a 0 there
        $('input[name=' + fieldName + ']').val(0);
    }
});

$('.cart-rec').owlCarousel({
    loop: true,
    margin: 0,
    nav: true,
    dots: false,
    responsive: {
        0: {
            items: 1
        },
        600: {
            items: 2
        },
        1000: {
            items: 3
        }
    }
});
