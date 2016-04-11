/**
 * Created by alexy on 28.05.15.
 */
$(function() {

  var current_url = '/'+location.href.split('/')[3]+'/' + location.href.split('/')[4] + '/';
  $('header ul li a').each(function () {
    if($(this).attr('href') == current_url) $(this).parent('li').addClass('active');
  });

  $.validator.messages.required = "* поле обязательно для заполнения";

  // ajax удаление объектов
  var fancy_initial = function(){
    $('.js-ajax-remove-btn').fancybox({
      afterClose: function () {
        $('.js-ajax-remove-item-form').resetForm();
      },
      beforeLoad: function() {
        var item_id = '#' + this.element[0].id;
        var item = $(item_id);
        $('#js-ajax-item-remove-id').val(item.parents('tr').data('id'));
        $('#js-ajax-item-remove-name').text(item.parents('tr').data('name'));
        $('#js-ajax-item-remove-model').val(item.parents('tr').data('model'));
       }
    });
  };
  $('.js-list').on('click', '.js-ajax-remove-btn', function(){
    fancy_initial();
  });

  $('.js-ajax-remove-item-form').ajaxForm({
    success: function(data){
      if (data.id) {
        $.notify('Объект был удалён', 'success');
        console.log($('#id_'+data.model+'_'+data.id));
        $('#id_'+data.model+'_'+data.id).remove();
        $.fancybox.close();
      } else {
        $.notify('Произошла ошибка. Объект не удалён', 'error');
        $.fancybox.close();
      }
      $('.js-ajax-remove-item-form').resetForm();
    }
  });
  $('.js-ajax-remove-item-form input[type="reset"]').click(function(){
    $.fancybox.close();
  });
  $('.js-ajax-remove-item-form input[type="submit"]').click(function(){
    $.fancybox.close();
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

  // валидация формы добавления пользователя
  $( '#js-form-user-add' ).validate({
    rules: {
      email: {
        required: true
      },
      last_name: {
        required: true
      },
      first_name: {
        required: true
      },
      phone: {
        required: true
      },
      password1: {
        required: true
      },
      password2: {
        required: true
      }
    },
    messages: {
      last_name: "Пожалуйста укажите фамилию",
      first_name: "Пожалуйста укажите имя",
      email: {
        required: "Вы не указали e-mail. Значение этого поля будет использоваться для входа в систему",
        email: "email должен иметь формат name@domain.com"
      }
    }
  });
  // валидация формы изменения пользователя
  $( '#js-form-user-update' ).validate({
    rules: {
      email: {
        required: true
      },
      last_name: {
        required: true
      },
      first_name: {
        required: true
      }
    },
    messages: {
      last_name: "Пожалуйста укажите фамилию",
      first_name: "Пожалуйста укажите имя",
      email: {
        required: "Вы не указали e-mail. Значение этого поля будет использоваться для входа в систему",
        email: "email должен иметь формат name@domain.com"
      }
    }
  });

  // валидация формы добавления/изменения города
  $( '#js-city-form' ).validate({
    rules: {
      name: {
        required: true
      }
    }
  });

  // Валидация форма изменения модератора
  $('#js-form-moderator-update').validate({
    rules: {
      moderator: {
        required: true
      },
      company: {
        required: true
      }
    },
    submitHandler: function(e) {
      $('#js-form-moderator-update').ajaxSubmit({
          success: function(data){
            if (data.success) {
              $.notify('Изменения успешно сохранены', 'success');
            } else {
              $.notify('Произошла ошибка! Проверьте правильность введённых данных', 'error');
            }
          }
      });
    }
  });

  // Валидация формы дбавления менеджера
  $('#js-form-manager-add').validate({
    rules: {
      moderator: {
        required: true
      },
      email: {
        required: true
      },
      last_name: {
        required: true
      },
      first_name: {
        required: true
      },
      password1: {
        required: true
      },
      password2: {
        required: true
      }
    },
    messages: {
      last_name: "Пожалуйста укажите фамилию",
      first_name: "Пожалуйста укажите имя",
      email: {
        required: "Вы не указали e-mail. Значение этого поля будет использоваться для входа в систему",
        email: "email должен иметь формат name@domain.com"
      }
    }
  });
  // Валидация формы редактирования менеджера
  $('#js-form-manager-update').validate({
    rules: {
      moderator: {
        required: true
      },
      email: {
        required: true,
        email: true
      },
      last_name: {
        required: true
      },
      first_name: {
        required: true
      }
    },
    messages: {
      last_name: "Пожалуйста укажите фамилию",
      first_name: "Пожалуйста укажите имя",
      email: {
        required: "Вы не указали e-mail. Значение этого поля будет использоваться для входа в систему",
        email: "email должен иметь формат name@domain.com"
      }
    }
  });

  // Валидация формы добавления продажи
  $('#js-form-sale-add').validate({
    rules: {
      moderator: {
        required: true
      },
      email: {
        required: true,
        email: true
      },
      last_name: {
        required: true
      },
      first_name: {
        required: true
      },
      password1: {
        required: true
      },
      password2: {
        required: true
      },
      legal_name: {
        required: true
      },
      city: {
        required: true
      }
    },
    messages: {
      last_name: "Пожалуйста укажите фамилию",
      first_name: "Пожалуйста укажите имя",
      email: {
        required: "Вы не указали e-mail. Значение этого поля будет использоваться для входа в систему",
        email: "email должен иметь формат name@domain.com"
      }
    }
  });

  // Валидация формы редактирования продажи
  $('#js-form-sale-update').validate({
    rules: {
      legal_name: {
        required: true
      },
      city: {
        required: true
      },
      manager: {
        required: true
      }
    },
    submitHandler: function(e) {
      $('#js-form-sale-update').ajaxSubmit({
          success: function(data){
            if (data.success) {
              $.notify('Изменения успешно сохранены', 'success');
            } else {
              $.notify('Произошла ошибка! Проверьте правильность введённых данных', 'error');
            }
          }
      });
    }
  });

  // валидация формы заказа по продаже
  $('#js-form-sale-order').validate({
    rules: {
      sale: {
        required: true
      },
      date_start: {
        required: true
      },
      count: {
        required: true
      },
      cost: {
        required: true
      }
    }
  });

  // валидация формы макета по продаже
  $('#js-form-sale-maket').validate({
    rules: {
      sale: {
        required: true
      },
      name: {
        required: true
      },
      date: {
        required: true
      },
      file: {
        required: true
      }
    }
  });

  // Валидация формы добавления распространителя
  $('#js-form-distributor-add').validate({
    rules: {
      moderator: {
        required: true
      },
      email: {
        required: true,
        email: true
      },
      last_name: {
        required: true
      },
      first_name: {
        required: true
      },
      password1: {
        required: true
      },
      password2: {
        required: true
      }
    }
  });
  // Валидация формы редактирования распространителя
  $('#js-form-distributor-update').validate({
    rules: {
      moderator: {
        required: true
      },
      email: {
        required: true,
        email: true
      },
      last_name: {
        required: true
      },
      first_name: {
        required: true
      }
    },
    messages: {
      last_name: "Пожалуйста укажите фамилию",
      first_name: "Пожалуйста укажите имя",
      email: {
        required: "Вы не указали e-mail. Значение этого поля будет использоваться для входа в систему",
        email: "email должен иметь формат name@domain.com"
      }
    }
  });

  // Валидация формы добавление клиента в CRM
  $('#js-form-client-add').validate({
    rules: {
      moderator: {
        required: true
      },
      manager: {
        required: true,
      },
      city: {
        required: true
      },
      name: {
        required: true
      }
    }
  });

  //  модальное окно переназначения менеджера в crm
  var reassign_manager_form = $('#js-form-reassign-manager');
  var reassign_fancy_initial = function() {
    $('.js-reassign-manager').fancybox({
      afterClose: function () {
        reassign_manager_form.resetForm();
      },
      beforeLoad: function () {
        var item_id = '#' + this.element[0].id;
        var item = $(item_id);
        var manager_name = item.parents('td').attr('data-manager-name');
        //var manager_name = item.prev('.js-manager-name').text();
        var manager_id = item.parents('td').attr('data-manager-id');
        var client = item.parents('tr').attr('data-id');
        reassign_manager_form.find('input[name=manager_name]').val(manager_name);
        reassign_manager_form.find('input[name=manager]').val(manager_id);
        reassign_manager_form.find('input[name=client]').val(client);
        $.ajax({
          type: "GET",
          data: {
            manager: item.parents('td').data('manager-id')
          },
          url: item.parents('td').data('url')
        }).done(function (data) {
          var manager_list = data.manager_list;
          var manager_list_selector = $('#js-manager-list');
          manager_list_selector.find('option').remove();
          manager_list_selector.append($("<option value selected='selected'>---------</option>"));
          for (var i = 0; i < manager_list.length; i++) {
            manager_list_selector.append($("<option/>", {
              value: manager_list[i]['id'],
              text: manager_list[i]['name']
            }));
          }
        });
      }
    });
  };
  $('.js-list').on('click', '.js-reassign-manager', function(){
    reassign_fancy_initial();
  });
  reassign_manager_form.validate({
    rules: {
      manager: {
        required: true
      },
      new_manager: {
        required: true
      }
    }
  });
  reassign_manager_form.ajaxForm({
    success: function(data){
      if (data.success) {
        $.notify('Менеджер был переназначен', 'success');
        var td_selector = $('tr[data-id="' + data.client_id +'"] td[data-manager-id="'+data.old_id+'"]');
        td_selector.find('.js-manager-name').text(data.name);
        td_selector.attr('data-manager-id', data.id);
        td_selector.attr('data-manager-name', data.name);
        $.fancybox.close();
      } else {
        $.notify('Произошла ошибка. Возможно вы не выбрали нового менеджера', 'error');
      }
      reassign_manager_form.resetForm();
      //reassign_fancy_initial();
    }
  });

  // модальное окно показа списка контактных лиц клиента
  $('.js-show-client-contact').fancybox({
      afterClose: function () {
        $('#js-client-contact-list').html('');
      },
      beforeLoad: function () {
        var item_id = '#' + this.element[0].id;
        var item = $(item_id);
        console.log(item.data('client'));

        $.ajax({
          type: "GET",
          url: item.data('url'),
          data: {
            client: item.data('client')
          }
        }).done(function (data) {
          if (data.contact_list) {
            var contact_list = data.contact_list;
            //var manager_list_selector = $('#js-manager-list');
            //manager_list_selector.find('option').remove();
            //manager_list_selector.append($("<option value selected='selected'>---------</option>"));
            for (var i = 0; i < contact_list.length; i++) {
              $('#js-client-contact-list').append(
                '<tr>' +
                  '<td>' + contact_list[i]['name'] + '</td>' +
                  '<td>' + contact_list[i]['function'] +
                  '<td>' + contact_list[i]['phone'] + '</td>' +
                  '<td>' + contact_list[i]['email'] + '</td>' +
                '</tr>'
              );
              console.log(contact_list[i]['name']);
              console.log(contact_list[i]['function']);
              console.log(contact_list[i]['phone']);
              console.log(contact_list[i]['email']);
            }
          } else {
            $('#js-client-contact-list').html('<tr><td colspan="4">Контактных лиц не найдено</td></tr>');
          }
        });
      }
    });

  // CRM Валидация формы добавления задачи клиенту
  $('#js-form-task-add').validate({
    rules: {
      manager: {
        required: true
      },
      client: {
        required: true
      },
      type: {
        required: true
      },
      date: {
        required: true
      }
    }
  });
  // CRM Валидация формы редактирования задачи по клиенту
  $('#js-form-task-update').validate({
    rules: {
      manager: {
        required: true
      },
      client: {
        required: true
      },
      type: {
        required: true
      },
      date: {
        required: true
      }
    }
  });

  // CRM  модальное окно формы создания задачи по клиенту
  $('.js-new-task-btn').fancybox({
    beforeLoad: function () {
      var item_id = '#' + this.element[0].id;
      var item = $(item_id);
      console.log(item.parents('tr').data('id'));
      $.ajax({
        type: "GET",
        url: item.data('url'),
        data: {
          client: item.parents('tr').data('id')
        }
      }).done(function (data) {
        console.log(data.id);
        console.log(data.type);
        console.log(data.name);
        var form = $('#js-task-modal-add-form');
        form.find('#id_client_type').text(data.type);
        form.find('#id_client_name').text(data.name);
        form.find('#id_client_id').val(data.id);
        var contact_list = data.contact_list;
        var contact_list_selector = form.find('#id_client_contact');
        contact_list_selector.find('option').remove();
        contact_list_selector.append($("<option value selected='selected'>---------</option>"));
        for (var i = 0; i < contact_list.length; i++) {
          contact_list_selector.append($("<option/>", {
            value: contact_list[i]['id'],
            text: contact_list[i]['name']
          }));
        }
      });
    }
  });
  $('#js-task-modal-add-form').ajaxForm({
    success: function(data){
      if (data.success) {
        $.notify('Задача по клиенту добавлена', 'success');
        $.fancybox.close();
      }
    }
  });
  // CRM  валидация модальной формы создания задачи
  $('#js-task-modal-add-form').validate({
    rules: {
      manager: {
        required: true
      },
      client: {
        required: true
      },
      client_contact: {
        required: true
      },
      type: {
        required: true
      },
      date: {
        required: true
      }
    }
  });

  // CRM валидация модальной формы редактирования задачи в журнале задач
  var validator = $('#js-task-modal-update-form').validate({
    rules: {
      client_contact: {
        required: true
      },
      type: {
        required: true
      },
      date: {
        required: true
      }
    }
  });
  // валидация формы редактирования задачи
  var sale_modal_validator = $('#js-ajax-sale-add').validate({
    rules: {
      email: {
        required: true
      },
      password: {
        required: true
      }
    }
  });

  // CRM модальное окно формы редактирования задачи по клиенту
  $('.js-change-task-btn').fancybox({
    afterClose: function () {
      validator.resetForm();
      sale_modal_validator.resetForm();
    },
    beforeLoad: function () {
      var item_id = '#' + this.element[0].id;
      var item = $(item_id);
      console.log(item);
      console.log(item.parents('tr').data('id'));
      $.ajax({
        type: "GET",
        url: item.data('url'),
        data: {
          task: item.parents('tr').data('id')
        }
      }).done(function (data) {
        console.log('id задачи' + data.task_id);
        console.log('id клиента' + data.client_id);
        console.log('название клиента' + data.client_name);
        console.log('тип клиента' + data.client_type);
        console.log('id менеджера' + data.manager_id);
        console.log('список контактных лиц' + data.contact_list);
        var form = $('#js-task-modal-update-form');
        form.find('#id_client_type').text(data.client_type);
        form.find('#id_client_name').text(data.client_name);
        form.find('#id_client').val(data.client_id);
        form.find('#id_task').val(data.task_id);
        form.find('#id_manager').val(data.manager_id);
        var contact_list = data.contact_list;
          var contact_list_selector = form.find('#id_client_contact');
          contact_list_selector.find('option').remove();
          contact_list_selector.append($("<option value>---------</option>"));
          for (var i = 0; i < contact_list.length; i++) {
            contact_list_selector.append($("<option/>", {
              value: contact_list[i]['id'],
              text: contact_list[i]['name']
            }));
          }
      });
    }
  });
  // ajax форма редактирования задачи
  $('#js-task-modal-update-form').ajaxForm({
    success: function(data){
      if (data.success) {
        $.notify('Задача по клиенту обновлена', 'success');
        $.fancybox.close();
        location.reload();
      } else {
        $.notify('Произошла ошибка', 'error');
      }
    }
  });

  // модальная форма создания продажи из задачи
  $('#js-ajax-sale-btn').on('click', function(){
    console.log('ПРОДАЖА!');
    var form = $('#js-task-modal-update-form');
    var manager = form.find('#id_manager').val();
    console.log('manager: '+ manager);
    var client = form.find('#id_client').val();
    console.log('client: ' + client);
    var comment = form.find('#id_comment').val();
    console.log('comment: ' + comment);
    var date = form.find('#id_date').val();
    console.log('date: ' + date);
    var contact = form.find('#id_client_contact').val();
    console.log('contact: ' + contact);
    var task = form.find('#id_task').val();
    console.log('task: ' + task);
    var client_type = form.find('#id_client_type').text();
    console.log('client_type: ' + client_type);
    var client_name = form.find('#id_client_name').text();
    console.log('client_name: ' + client_name);

    var c_form = $('#js-ajax-sale-add');
    console.log(c_form);
    c_form.find('#id_client').val(client);
    c_form.find('#id_manager').val(manager);
    c_form.find('#id_task').val(task);
    c_form.find('#id_comment').val(comment);
    c_form.find('#id_date').val(date);
    c_form.find('#id_contact').val(contact);
    c_form.find('#id_sale_name').text(client_name);
    c_form.find('#id_client_type').text(client_type);


    $('.sale-modal-add-form').toggle();
    $('.task-modal-update-form').toggle();
    $('.task-modal-text').toggle();
    $('.sale-modal-add-text').toggle();

  });
  $('#js-back-to-task-modal-update-form').on('click', function(){
    $('.sale-modal-add-form').toggle();
    $('.task-modal-update-form').toggle();
    $('.task-modal-text').toggle();
    $('.sale-modal-add-text').toggle();
  });

  // Развернуть карту на странице со списком городов
  $('.js-show-map').click(function(){
    $('.js-map').slideToggle();
  });

  // валидация формы района города модератора
  $('#js-form-moderatorarea').validate({
    rules: {
      city: {
        required: true
      },
      moderator: {
        required: true
      },
      name: {
        required: true
      }
    }
  });














  // ДАЛЕЕ ИДЁТ СТАРЫЙ КОД!








  // ajax форма редактирования задачи
  //$('#js-ajax-client-add').ajaxForm({
  //  success: function (data) {
  //    if (data.error) {
  //      $.notify('Клиент с таким e-mail уже зарегистрирован в системе', 'error');
  //      $.fancybox.close();
  //    }
  //  }
  //});
  var ia_form = $('#js-form-incomingtask-add');
  ia_form.find('#id_incomingclient').change(function(){
    var client = $(this).val();
    var url = $(this).parents('.form-group').data('url');
    console.log(url);
    var clientcontact_selector = ia_form.find('#id_incomingclientcontact');
    if (client) {
      console.log(client);
      clientcontact_selector.parents('.form-group').removeClass('hide');
      $.ajax({
        type: "GET",
        url: url,
        data: {
          incomingclient: client
        }
      }).done(function (data) {
        if (data.contact_list) {
          var contact_list = data.contact_list;
          console.log(contact_list);
          clientcontact_selector.find('option').remove();
          clientcontact_selector.append($("<option value selected='selected'>---------</option>"));
          for (var i = 0; i < contact_list.length; i++) {
            clientcontact_selector.append($("<option/>", {
              value: contact_list[i]['id'],
              text: contact_list[i]['name']
            }));
          }

        } else {
          clientcontact_selector.find('option').remove();
        }
      });
    } else {
      console.log('empty');
      clientcontact_selector.find('option').remove();
      clientcontact_selector.parents('.form-group').addClass('hide');
    }
  })
});