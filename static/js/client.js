/**
 * Created by alexy on 31.10.16.
 */
$(function() {
  $.validator.messages.required = "* обязательное поле";
  $('.js-questionary-link').fancybox({
    type: 'iframe',
    helpers: {
      overlay: {
        locked: false
      }
    }
  });

  $('#js-photo-map-button').click(function(){
    $('.map-wrapper').slideToggle();
    $('.client-nav').toggleClass('client-nav_mb')
  });
  $('#js-photo-map-close').click(function(){
    $('.map-wrapper').slideUp();
    $('.client-nav').removeClass('client-nav_mb')
  });
  $('.js-filter-show').click(function(){
    $('.client-search-form').toggleClass('hidden-xs');
    $('.client-search-form').toggleClass('hidden-sm');
  });
  $('.js-show-mobile-menu').click(function(){
    $('.mobile-menu').fadeToggle();
  });
  $('.js-close-mobile-menu').click(function(){
    $('.mobile-menu').fadeToggle();
  });

  $(".js-gallery").fancybox({
    helpers: {
      overlay: {
        locked: false
      }
    }
  });
  $(".js-show-modal-review-btn").fancybox({
    beforeLoad: function() {
      $('.mobile-menu').hide();
    },
    helpers: {
      overlay: {
        locked: false
      }
    }
  });
  var sale_dash_form = $("#js-sale-dash-form");
  sale_dash_form.find("#id_date_start").datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  sale_dash_form.find("#id_date_end").datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  $('#js-page-count').change(function(){
    $('#id_page_count').val($(this).val());
    $(this).parents('form').submit();
  });
  // валидация формы добавления отзыва
  $('#js-form-review-add').validate({
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
    },
    submitHandler: function(e) {
      $('#js-form-review-add').ajaxSubmit({
          success: function(data){
            if (data.success) {
              $.fancybox.close();
              $.notify('Спасибо за ваш отзыв', 'success');
            } else {
              $.notify('Произошла ошибка! Проверьте правильность введённых данных', 'error');
            }
          }
      });
    }
  });
});