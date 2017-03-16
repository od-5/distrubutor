/**
 * Created by alexy on 28.05.15.
 */
$(function() {

  var current_url = '/'+location.href.split('/')[3]+'/' + location.href.split('/')[4] + '/';
  $('header ul li a').each(function () {
    if($(this).attr('href') == current_url) $(this).parent('li').addClass('active');
  });

  $.validator.messages.required = "* поле обязательно для заполнения";


  // Показать\скрыть поиск
  $('#js-show-filter-btn').click(function(){
    $('.form-filter').slideToggle();
    $('#js-show-filter-btn').find('span').toggleClass('hide');
  });
  // Мобильные меню
  // Закрыть меню
  $('.js-dashboard-modal-close').click(function(){
    $('.dashboard-modal-profile').fadeOut();
    $('.dashboard-modal-menu').fadeOut();
  });
  // Открыть меню пользователя
  $('.js-dashboard-mobile-profile__btn').click(function(){
    $('.dashboard-modal-profile').fadeIn();
  });
  // Открыть меню навигации
  $('.js-dashboard-mobile-menu__btn').click(function(){
    $('.dashboard-modal-menu').fadeIn();
  });


  // показать\спрятать кнопку добавления оплаты
  $('.saleorder-tr').hover(
    function(){
      $(this).find('.js-payment-add-btn').removeClass('hide');
    },
    function() {
      $(this).find('.js-payment-add-btn').addClass('hide')
    }
  );

  //валидация формы создания рассылки по хенгерам
  $('#js-form-hangermail').validate({
    rules: {
      moderator: {
        required: true
      },
      city: {
        required: true
      },
      title: {
        required: true
      },
      phone: {
        required: true
      },
      count: {
        required: true
      },
      price: {
        required: true
      }
    }
  });
  // валидация формы создания вёрстки
  $('#js-form-stand-add').validate({
    rules: {
      moderator: {
        required: true
      },
      date_start: {
        required: true
      },
      date_end: {
        required: true
      }
    }
  });
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
    helpers: {
      overlay: {
        locked: false
      }
    },
    afterClose: function () {
      $('.js-modal-payment-add-form').resetForm();
    },
    beforeLoad: function() {
      var item_id = '#' + this.element[0].id;
      var item = $(item_id);
      var form = $('.js-modal-payment-add-form');
      form.find('#p_sale').val(item.data('sale'));
      form.find('#p_saleorder').val(item.data('saleorder'));
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
      helpers: {
        overlay: {
          locked: false
        }
      },
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

  // Валидация формы добавления заявки внутри кабинета
  $('#js-form-ticket-add').validate({
    rules: {
      city: {
        required: true
      },
      moderator: {
        required: true
      },
      name: {
        required: true
      },
      mail: {
        required: true
      },
      phone: {
        required: true
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

  // валидация формы добавления/изменения страны
  $('#js-country-form').validate({
    rules: {
      name: {
        required: true
      },
      code: {
        required: true
      }
    }
  });

  // валидация формы добавления/изменения региона
  $('#js-region-form').validate({
    rules: {
      country: {
        required: true
      },
      name: {
        required: true
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
  var sale_order_form = $('#js-form-sale-order');
  // отображение\сркытие полей в форме заказа при выборе категорий заказа
  sale_order_form.find('#id_category').change(function(){
    var category = $(this).val();
    if (category == 2) {
        sale_order_form.find('#id_questionary').rules('add', {'required': true});
        sale_order_form.find('#id_questionary').parents('.form-group').removeClass('hide');
    } else {
        sale_order_form.find('#id_questionary').rules('remove');
        sale_order_form.find('#id_questionary').parents('.form-group').addClass('hide');
    }
    if (category != 0) {
      sale_order_form.find('#id_type').rules('remove', 'required');
      sale_order_form.find('#id_type').parents('.form-group').addClass('hide');
    } else {
      sale_order_form.find('#id_type').rules('add', {'required': true});
      sale_order_form.find('#id_type').parents('.form-group').removeClass('hide');
    }
  });
  // валидация формы заказа по продаже
  sale_order_form.validate({
    rules: {
      sale: {
        required: true
      },
      category: {
        required: true
      },
      type: {
        required: true
      },
      questionary: {
        required: true
      },
      date_start: {
        required: true
      },
      date_end: {
        required: true
      }
    },
    messages: {
      type: {
        required: '* вы не выбрали тип заказа!'
      },
      questionary: {
        required: '* вы не выбрали анкету!'
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
      helpers: {
        overlay: {
          locked: false
        }
      },
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
      helpers: {
        overlay: {
          locked: false
        }
      },
      afterClose: function () {
        $('#js-client-contact-list').html('');
      },
      beforeLoad: function () {
        var item_id = '#' + this.element[0].id;
        var item = $(item_id);

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
    helpers: {
      overlay: {
        locked: false
      }
    },
    beforeLoad: function () {
      var item_id = '#' + this.element[0].id;
      var item = $(item_id);
      $.ajax({
        type: "GET",
        url: item.data('url'),
        data: {
          client: item.parents('tr').data('id')
        }
      }).done(function (data) {
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
    beforeSubmit: function(arr, $form, options) {
      //alert('hay');
      $form.find('input[type=submit]').attr('disabled', 'disabled');
        // The array of form data takes the following form:
        // [ { name: 'username', value: 'jresig' }, { name: 'password', value: 'secret' } ]

        // return false to cancel submit
    },
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
    helpers: {
      overlay: {
        locked: false
      }
    },
    afterClose: function () {
      validator.resetForm();
      sale_modal_validator.resetForm();
    },
    beforeLoad: function () {
      var item_id = '#' + this.element[0].id;
      var item = $(item_id);
      $.ajax({
        type: "GET",
        url: item.data('url'),
        data: {
          task: item.parents('tr').data('id')
        }
      }).done(function (data) {
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
    var form = $('#js-task-modal-update-form');
    var manager = form.find('#id_manager').val();
    var client = form.find('#id_client').val();
    var comment = form.find('#id_comment').val();
    var date = form.find('#id_date').val();
    var contact = form.find('#id_client_contact').val();
    var task = form.find('#id_task').val();
    var client_type = form.find('#id_client_type').text();
    var client_name = form.find('#id_client_name').text();

    var c_form = $('#js-ajax-sale-add');
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





  $(".js-gallery").fancybox({
    helpers: {
      overlay: {
        locked: false
      }
    }
  });

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

//  Удаление фотографий на странице редактирования контрольной точки
  $('.js-photo-remove-btn').click(function(){
    var photo_id = $(this).data('id');
    $(this).parents('#js-photo-container').find('.photo-delete-block').slideToggle();

  });
  $('.js-photo-remove-reset').click(function(){
    $('.photo-delete-block').slideUp()
  });
  $('.js-photo-remove-confirm').click(function(){
    var url = $(this).data('url');
    var photo_id = $(this).data('id');
    var container = $(this).parents('#js-photo-container');
    $.ajax({
      type: "GET",
      data: {
        photo_id: photo_id
      },
      url: url
    }).done(function (data) {
      if(data.success){
        container.remove();
        $.notify('Фотография удалена', 'success');
      } else {
        $.notify('Произошла ошибка. Обновите страницу и попробуйте ещё раз', 'error');
      }
    });
    container.find('.photo-delete-block').slideUp();
  });
  // выбор всех менеджеров на странице отчёта
  var table_report = $('.js-table-report');
  table_report.find('#js-select-all');
  table_report.find('#js-select-all').on('click', function(){
    table_report.find('tbody input[type=checkbox]').prop('checked', $(this).prop('checked'));
  });

  // отправка смс уедомления
  $('#js-sale-send-sms').ajaxForm({
    success: function(data){
      if (data.success) {
        $.notify('СМС с логином и паролем успешно отправлено клиенту', 'success');
      } else {
        $.notify('СМС не может быть отправлено', 'error');
      }
    }
  });

  // отправка email уедомления
  $('.js-sale-send-email').ajaxForm({
    success: function(data){
      if (data.success) {
        $.notify('Email уведоление о выполнении заказа успешно отправлено клиенту', 'success');
      } else {
        $.notify('Email уведоление не может быть отправлено', 'error');
      }
    }
  });


});
