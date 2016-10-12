/**
 * Created by alexy on 28.05.15.
 */
$(function() {

  var current_url = '/'+location.href.split('/')[3]+'/' + location.href.split('/')[4] + '/';
  $('header ul li a').each(function () {
    if($(this).attr('href') == current_url) $(this).parent('li').addClass('active');
  });

  $.validator.messages.required = "* поле обязательно для заполнения";

  // показать\спрятать кнопку добавления оплаты
  $('.saleorder-tr').hover(
    function(){
      $(this).find('.js-payment-add-btn').removeClass('hide');
    },
    function() {
      $(this).find('.js-payment-add-btn').addClass('hide')
    }
  );
  // валидация формы добавления оплаты
  $( '.js-modal-payment-add-form' ).validate({
    rules: {
      p_sale: {
        required: true
      },
      p_saleorder: {
        required: true
      },
      p_sum: {
        required: true,
        number: true
      }
    }
  });
  // форма добавления оплаты
  $('.js-payment-add-btn').fancybox({
    afterClose: function () {
      $('.js-modal-payment-add-form').resetForm();
    },
    beforeLoad: function() {
      var item_id = '#' + this.element[0].id;
      var item = $(item_id);
      var form = $('.js-modal-payment-add-form');
      console.log(item);
      console.log(item.data('sale'));
      console.log(item.data('saleorder'));
      form.find('#p_sale').val(item.data('sale'));
      form.find('#p_saleorder').val(item.data('saleorder'));
      console.log('sale' + form.find('#p_sale').val());
      console.log('saleorder' + form.find('#p_saleorder').val());
     }
  });
  $('.js-modal-payment-add-form').ajaxForm({
    success: function (data) {
      if (data.success) {
        $.notify('Оплата сохранена. Идёт пересчёт поступлений.', 'success');
        $.fancybox.close();
        location.reload();
      } else {
        $.notify('Произошла ошибка. Оплата не сохранена', 'error');
        $.fancybox.close();
      }
    }
  });
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
        if ($('tr').is('#id_'+data.model+'_'+data.id+'_photo')){
          $('#id_'+data.model+'_'+data.id+'_photo').remove();
        }
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
      country: {
        required: true
      },
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
    messages: {
      fb_link: {
        url: 'Адрес должен начинаться с http://'
      },
      vk_link: {
        url: 'Адрес должен начинаться с http://'
      },
      ok_link: {
        url: 'Адрес должен начинаться с http://'
      },
      insta_link: {
        url: 'Адрес должен начинаться с http://'
      }
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
      type: {
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
    },
    messages: {
      type: {
        required: '* вы не выбрали тип заказа!'
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
  // Валидация формы редактирования оплаты распространителю
  $('#js-form-distributor-payment').validate({
    rules: {
      cost: {
        required: true,
        number: true
      },
      type: {
        required: true,
        number: true
      }
    },
    submitHandler: function(e) {
      $('#js-form-distributor-payment').ajaxSubmit({
          success: function(data){
            if (data.success) {
              $.notify(data.success, 'success');
            } else {
              $.notify(data.error, 'error');
            }
          }
      });
    }
  });



  // Валидация формы добавление клиента в CRM
  $('#js-form-client-add').validate({
    rules: {
      moderator: {
        required: true
      },
      manager: {
        required: true
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
    beforeSubmit: function(arr, $form, options) {
      $form.find('input[type=submit]').attr('disabled', 'disabled');
    },
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

  // валидация формы добавления задачи для распространителя
  var d_t_a_form = $('#js-form-distributor-task-add');
  d_t_a_form.validate({
    rules: {
      distributor: {
        required: true
      },
      sale: {
        required: true
      },
      order: {
        required: true
      },
      area: {
        required: true
      },
      material_count: {
        required: true,
        number: true
      },
      date: {
        required: true
      }
    },
    messages: {
      material_count: {
        required: "Введите число.",
        number: "Введите число."
      }
    }
  });
  d_t_a_form.find('#id_sale').change(function(){
    var distributor = d_t_a_form.find('#id_distributor');
    var area = d_t_a_form.find('#id_area');
    var order = d_t_a_form.find('#id_order');
    var url = $(this).parents('.form-group').data('url');
    if($(this).val()){
      $.ajax({
        type: "GET",
        url: url,
        data: {
          sale: $(this).val()
        }
      }).done(function (data) {
        if(data.error){
          $.notify(data.error, 'success');
        } else {
          var distributor_list = data.distributor_list;
          var area_list = data.area_list;
          var order_list = data.order_list;
          distributor.find('option').remove();
          distributor.append($("<option value selected='selected'>---------</option>"));
          for (var i = 0; i < distributor_list.length; i++) {
            distributor.append($("<option/>", {
              value: distributor_list[i]['id'],
              text: distributor_list[i]['name']
            }));
          }
          area.find('option').remove();
          area.append($("<option value selected='selected'>---------</option>"));
          for (var j = 0; j < area_list.length; j++) {
            area.append($("<option/>", {
              value: area_list[j]['id'],
              text: area_list[j]['name']
            }));
          }
          order.find('option').remove();
          order.append($("<option value selected='selected'>---------</option>"));
          for (var k = 0; k < order_list.length; k++) {
            order.append($("<option/>", {
              value: order_list[k]['id'],
              text: order_list[k]['name']
            }));
          }
        }

      });

      distributor.parents('.form-group').removeClass('hide');
      area.parents('.form-group').removeClass('hide');
      order.parents('.form-group').removeClass('hide');
    } else {
      distributor.find('option').remove();
      area.find('option').remove();
      order.find('option').remove();
      distributor.parents('.form-group').addClass('hide');
      area.parents('.form-group').addClass('hide');
      order.parents('.form-group').addClass('hide');
    }
  });

  // валидация формы редактирования задачи для распространителя
  var d_t_u_form = $('#js-form-distributor-task-update');
  d_t_u_form.validate({
    rules: {
      distributor: {
        required: true
      },
      sale: {
        required: true
      },
      order: {
        required: true
      },
      area: {
        required: true
      },
      //type: {
      //  required: true
      //},
      material_count: {
        required: true,
        number: true
      },
      date: {
        required: true
      }
    },
    messages: {
      material_count: {
        required: "Введите число.",
        number: "Введите число."
      }
    }
  });
  d_t_u_form.find('#id_sale').change(function(){
    var distributor = d_t_u_form.find('#id_distributor');
    var area = d_t_u_form.find('#id_area');
    var order = d_t_u_form.find('#id_order');
    var url = $(this).parents('.form-group').data('url');
    if($(this).val()){
      $.ajax({
        type: "GET",
        url: url,
        data: {
          sale: $(this).val()
        }
      }).done(function (data) {
        if(data.error){
          $.notify(data.error, 'success');
        } else {
          var distributor_list = data.distributor_list;
          var area_list = data.area_list;
          var order_list = data.order_list;
          distributor.find('option').remove();
          distributor.append($("<option value selected='selected'>---------</option>"));
          for (var i = 0; i < distributor_list.length; i++) {
            distributor.append($("<option/>", {
              value: distributor_list[i]['id'],
              text: distributor_list[i]['name']
            }));
          }
          area.find('option').remove();
          area.append($("<option value selected='selected'>---------</option>"));
          for (var j = 0; j < area_list.length; j++) {
            area.append($("<option/>", {
              value: area_list[j]['id'],
              text: area_list[j]['name']
            }));
          }
          order.find('option').remove();
          order.append($("<option value selected='selected'>---------</option>"));
          for (var k = 0; k < order_list.length; k++) {
            area.append($("<option/>", {
              value: order_list[k]['id'],
              text: order_list[k]['name']
            }));
          }
        }

      });
    } else {
      distributor.find('option').remove();
      area.find('option').remove();
      order.find('option').remove();
    }
  });

  $(".js-gallery").fancybox();

  // Показать/скрыть календарь работ для распространителя
  $('.js-calendar-heading').click(function(){
    $('.js-calendar-body').slideToggle();
  });

  // Показать.скрыть panel-body по клику на panel-heading
  $('.js-toggle-heading').click(function(){
    $(this).next('.js-toggle-body').slideToggle();
  });

  // валидация формы настроек сайта
  $('#js-form-setup').validate({
    rules: {
      meta_title: {
        required: true
      },
      email: {
        required: true,
        email: true
      }
    },
    messages: {
      email: {
        required: "Вы не указали e-mail. На этот адрес будут приходит заявки с сайта",
        email: "email должен иметь формат name@domain.com"
      }
    }
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
    }
  });

  // валидация формы редактирования комментария
  $('#js-form-review-update').validate({
    rules: {
      moderator: {
        required: true
      },
      mail: {
        required: true,
        email: true
      },
      name: {
        required: true
      },
      text: {
        required: true
      }
    },
    messages: {
      mail: {
        required: "Вы не указали e-mail.",
        email: "e-mail должен иметь формат name@domain.com"
      }
    }
  });

});