/**
 * Created by alexy on 24.02.16.
 */
$(function() {
  //  Валидация формы создания ответа на сообщение
  $('.js-usermessageanswer-add-form').validate({
    rules: {
      text: {
        required: true
      },
      author: {
        required: true
      },
      recipient: {
        required: true
      },
      usermessage: {
        required: true
      }
    }
  });
  //  валидация формы создания рассылки
  var message_form = $('#js-message-form');
  message_form.validate({
    rules: {
      title: {
        required: true
      },
      text: {
        required: true
      }
    }
  });
  var check_sender_list = function() {
    var s_list = $('.js-sender-list__item');
    if (s_list.length) {
      message_form.find('button[type=submit]').removeAttr("disabled", "disabled");
      console.log(s_list.length);
    } else {
      message_form.find('button[type=submit]').attr("disabled", "disabled");
      console.log('nothing');
    }
  };
  // Получение списка модераторов по выбранному городу
  message_form.find('#id_city').change(function() {
    var city = $(this).val();
    var url = $(this).parents('.form-group').data('url');
    var moderator_table = $('.js-moderator-list');
    if (city == '') {
      moderator_table.find('tr.result').remove();
    } else {
      $.ajax({
        type: "GET",
        url: url,
        data: {
          city: city
        }
      }).done(function (data) {

        if (data.moderator_list) {
          var moderator_list = data.moderator_list;
          console.log(moderator_list);
          moderator_table.find('tr.result').remove();
          console.log(moderator_table);
          for (var i = 0; i < moderator_list.length; i++){
            moderator_table.append(
              '<tr class="result">'+
              '<td><input type="checkbox" name="chk_group[]" value="' + moderator_list[i]['id'] +'" data-name="' + moderator_list[i]['name'] + '"></td>'+
              '<td>'+moderator_list[i]['name']+'</td>'+
              '</tr>'
            )
          }
          var select_all_selector = $('#js-select-all');
          select_all_selector.prop('checked', false);
          select_all_selector.on('click', function(){
            moderator_table.find('tr.result input').prop('checked', $(this).prop('checked'));
          });
          $('.js-moderator-list input:checkbox').on('click', function(){
            if ($('.result input:checkbox:checked').length) {
              $('.js-add-to-sender-list__btn').removeClass('hide');
            } else {
              $('.js-add-to-sender-list__btn').addClass('hide');
            }
          });
          $('.js-add-to-sender-list__btn').click(function(){
            //var checked_list = $('.result input:checkbox:checked');

            $('.result input:checkbox:checked').each(function( index ) {
              // заполнение списка получателей
              var selector_id = '#js-sender-' + $( this ).val();
              console.log(selector_id);
              if ($("div").is(selector_id)) {
              } else {
                $('.js-sender-list').append(
                  '<div class="js-sender-list__item sender-list__item alert-info" id="js-sender-' + $( this ).val() + '">'+
                  '<input type="hidden" name="sender_group[]" value="' + $( this ).val() + '">' + $( this ).data('name') +
                  '<span class="text-danger glyphicon glyphicon-remove js-sender-remove"></span>'+
                  '</div>'
                );
                check_sender_list();
              }
            });

          //}
          });
        } else {
          moderator_table.find('tr.result').remove();
        }
      });
    }
  });

  //удаление получателя из списка
  $('.js-sender-list').on('click', '.js-sender-remove', function(){
    $(this).parents('.js-sender-list__item').remove();
    check_sender_list();
  });
  //$('.result input:checkbox').on('click', function(){
  //  if ($('.result input:checkbox:checked').length) {
  //    $('.js-add-to-sender-list__btn').removeClass('hide');
  //  } else {
  //    $('.js-add-to-sender-list__btn').addClass('hide');
  //  }
  //});
  //$('.js-moderator-list input:checkbox').on('click', function(){
  //  if ($('.result input:checkbox:checked').length) {
  //    $('.js-add-to-sender-list__btn').removeClass('hide');
  //  } else {
  //    $('.js-add-to-sender-list__btn').addClass('hide');
  //  }
  //});

});