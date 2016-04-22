$(document).ready(function () {

  $('.scroll a').each(function(){
    var some_id = $(this).attr('href').replace('#', '');
    $(this).addClass(some_id);
  });
  $(window).scroll( function(){
    if ($(this).scrollTop() > 50){
      $('.header-fix').addClass('fixed');
      $('.city-hidden').slideUp();
      $('.header-city a').removeClass('active');
    }else{
      $('.header-fix').removeClass('fixed');
    }

    var t = $(this).scrollTop() + 275;
    var sid = '';
    var lid = '';
    $('.scroll a').each(function(){
      var id = $(this).attr('href').replace('/', '');
      var o = $(id).offset().top;
      if(o < t){
        sid = id;
      }
    });
    var lid = sid.replace('#', '');
    $('.scroll a').removeClass('active');
    if(lid){
      $('.scroll a.' + lid).addClass('active');
    }

  });
  // scroll
  $('.scroll a').click(function(e){
    e.preventDefault();
     $.fancybox.close();
    var selected = $(this).attr('href').replace('/', '');
    $.scrollTo(selected, 1000, {offset: -0});
    return false;
  });


  // fancybox
  $('.fancybox').fancybox();
  $(".input[name='phone']").mask("+7 (999) 999-99-99");
  $('.ticket-form').each(function(){
    $(this).validate({
         rules: {
        name: {
          required: true
        },
        mail: {
          required: true,
          email: true
        },
        phone: {
          required: true,
          minlength: 6
        }
      }
      });
  });
  $('.ticket-form').ajaxForm({
    success: function(data){
      if (data.error) {
        $('form').resetForm();
        $.notify(data.error, 'error');
        console.log(data.error);
      } else {
        $('form').resetForm();
        $('#mask, .window').hide();
        $.notify(data.success, 'success');
        console.log('not error');
      }
    }
  });

  // header hidden
  $(document).on('click','.lang-link-top',function(e){
    e.preventDefault();
    if($(this).hasClass('active')){
      $(this).removeClass('active');
      $('.header-lang-hidden').slideUp();
    }else{
      $(this).addClass('active');
      $('.header-lang-hidden').slideDown();
    }
  });
  $(document).on('click','.enter-link-top',function(e){
    e.preventDefault();
    if($(this).hasClass('active')){
      $(this).removeClass('active');
      $('.header-enter-hidden').slideUp();
    }else{
      $(this).addClass('active');
      $('.header-enter-hidden').slideDown();
    }
  });
  // city hidden
  $(document).on('click','.header-city a',function(e){
    e.preventDefault();
    if($(this).hasClass('active')){
      $(this).removeClass('active');
      $('.city-hidden').slideUp();
    }else{
      $(this).addClass('active');
      $('.city-hidden').slideDown();
    }
  });
  $(document).on('click','.city-close',function(e){
    e.preventDefault();
    $('.city-hidden').slideUp();
    $('.header-city a').removeClass('active');
  });

  // slider
  $('.i-slider').bxSlider({
    pause: 5000,
    auto: false,
    prevText: 'предыдущий исполнитель',
    nextText: 'cледующий исполнитель',
    //mode: 'fade',
    speed: 1000,
    pager: true,
    pagerType: 'short',
    pagerShortSeparator: ' из ',
    controls: true,
    adaptiveHeight: true
  });

  // comment form
  $(document).on('click','.comment-button',function(e){
    e.preventDefault();
    var form = $(this).parent().find('.comment-form');
    if($(this).hasClass('comment-vis')){
      $('.comment-button').removeClass('comment-vis');
      $('.comment-form').slideUp();
    }else{
      $('.comment-button').removeClass('comment-vis');
      $('.comment-form').slideUp();
      $(form).slideDown();
      $(this).addClass('comment-vis').hide();
    }
  });



  //Скрипт всплывающих окон
  $('.modal').click(function(e) {
    e.preventDefault();
    $('#mask, .window').hide();
    var id = $(this).attr('href');
    var maskHeight = $(document).height();
    var maskWidth = $(window).width();
    $('#mask').css({'height':maskHeight});
    $('#mask').fadeTo("slow",0.9);
    var winH = $(window).height();
    var winW = $(window).width();
    $(id).css('top',  winH/2-$(id).height()/2);
    $(id).css('left', winW/2-$(id).width()/2);
    $(id).fadeIn(1000);
  });
  $('.window .close').click(function (e) {
    e.preventDefault();
    $('#mask, .window').hide();
  });
  $('#mask').click(function () {
    $(this).hide();
    $('.window').hide();
  });
  //Скрипт всплывающих окон
  //  обработка нажатия на город
  $('.city-list').find('a').click(function () {
    var url = $(this).parents('.city-list').data('url');
    var city = $(this).text();
    console.log(url);
    console.log(city);
    $.ajax({
      type: "POST",
      url: url,
      data: {
        city: city
      }
    }).done(function () {
      location.reload();
    });
  });

//  ввод города
  $('.input_city').each(function(){
    $(this).autocomplete({
      source: function(request, response){
        // организуем кроссдоменный запрос
        $.ajax({
          url: $('.input_city').data('url'),
          dataType: "json",
          // параметры запроса, передаваемые на сервер (последний - подстрока для поиска):
          data:{
            style: "full",
            maxRows: 12,
            name_startsWith: request.term
          },
          // обработка успешного выполнения запроса
          success: function(data){
            console.log(data);
            if(data.city_list.length){
              console.log('OK');
              $('.city-input-text').hide();
            }else {
              console.log('nothing');
              $('.city-input-text').show();
            }
            // приведем полученные данные к необходимому формату и передадим в предоставленную функцию response
            response($.map(data.city_list, function(item){
              return{
                label: item.name,
                value: item.name
              }
            }));
          }
        });
      },
      minLength: 2
    });
  });

  // Валидация формы добавления комментария
  $('.js-form-review-add').each(function(){
    $(this).validate({
      rules: {
        moderator: {
          required: true
        },
        name: {
          required: true
        },
        mail: {
          required: true,
          mail: true
        },
        text: {
          required: true
        },
        rating: {
          required: true
        }
      },
      messages: {
        mail: {
          required: "Вы не указали ваш e-mail.",
          email: "e-mail должен иметь формат name@domain.com"
        }
      }
    });
  });

});
