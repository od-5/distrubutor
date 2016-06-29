/**
 * Created by alexy on 24.06.16.
 */
$(function() {
  $('#js-show-menu').click(function(){
    $('.navbar').slideToggle();
  });

  $('#js-show-search').click(function(){
    $('.form-search').slideToggle();
    $(this).find('.glyphicon-chevron-down').toggleClass('hide');
    $(this).find('.glyphicon-chevron-up').toggleClass('hide');
  });
  var sale_photo_search_form = $('#js-sale-photo-search-form');
  sale_photo_search_form.find("#id_date_start").datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  sale_photo_search_form.find("#id_date_end").datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  // валидация профиля
  $('#js-form-profile-update').validate({
    rules: {
      email: {
        required: true
      }
    },
    messages: {
      email: {
        required: "Вы не указали e-mail. Значение этого поля будет использоваться для входа в систему",
        email: "email должен иметь формат name@domain.com"
      }
    }
  });
  // валидация формы изменения пароля
  $( '.js-form-password-change' ).validate({
    rules: {
      user_id: {
        required: true
      },
      password1: {
        required: true
      },
      password2: {
        required: true
      }
    },
    submitHandler: function(e) {
      $('.js-form-password-change').ajaxSubmit({
          success: function(data){
            if (data.success) {
              $.notify(data.success, 'success');
            } else {
              $.notify(data.error, 'error');
            }
            $('.js-form-password-change').trigger('reset');
          }
      });
    }
  });
});