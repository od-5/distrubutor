/**
 * Created by alexy on 12.07.16.
 */
$(function() {
  $.validator.messages.required = "* поле обязательно для заполнения";
  // валидация формы авторизации
  $( '#js-sign-form' ).validate({
    rules: {
      username: {
        required: true
      },
      password: {
        required: true
      }
    }
  });
});