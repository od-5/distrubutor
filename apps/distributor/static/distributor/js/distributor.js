/**
 * Created by alexy on 03.03.17.
 */
$(function(){
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
          sale: $(this).val(),
          category: d_t_a_form.find('#id_category').val()
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
              material: order_list[k]['material_residue'],
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
  d_t_a_form.find('#id_order').change(function(){
    var url = $(this).parents('.form-group').data('url');
    console.log($(this).val());
    var order = $(this).val();
    if($(this).val()){
      $.ajax({
        type: "GET",
        url: url,
        data: {
          order: order
        }
      }).done(function (data) {
        if(data.count){
          $('#js-order-material-residue').text('По заказу осталось распространить листовок: ' + data.count)
        } else {
          $('#js-order-material-residue').text('')
        }
      });
    } else {
      $('#js-order-material-residue').text('')
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
          sale: $(this).val(),
          category: d_t_u_form.find('#id_category').val()
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
    } else {
      distributor.find('option').remove();
      area.find('option').remove();
      order.find('option').remove();
    }
  });

  // валидация формы добавления задачи на проведение промо акции
  var d_t_p_a_form = $('#js-form-distributor-task-promo-add');
  d_t_p_a_form.validate({
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
      date: {
        required: true
      },
      coord_x: {
        required: true
      },
      coord_y: {
        required: true
      }
    }
  });
  d_t_p_a_form.find('#id_sale').change(function(){
    var distributor = d_t_p_a_form.find('#id_distributor');
    var order = d_t_p_a_form.find('#id_order');
    var url = $(this).parents('.form-group').data('url');
    if($(this).val()){
      $.ajax({
        type: "GET",
        url: url,
        data: {
          sale: $(this).val(),
          category: d_t_p_a_form.find('#id_category').val()
        }
      }).done(function (data) {
        if(data.error){
          $.notify(data.error, 'success');
        } else {
          var distributor_list = data.distributor_list;
          var order_list = data.order_list;
          distributor.find('option').remove();
          distributor.append($("<option value=''>---------</option>"));
          for (var i = 0; i < distributor_list.length; i++) {
            distributor.append($("<option/>", {
              value: distributor_list[i]['id'],
              text: distributor_list[i]['name']
            }));
          }
          order.find('option').remove();
          order.append($("<option value=''>---------</option>"));
          for (var k = 0; k < order_list.length; k++) {
            order.append(
              '<option value='+order_list[k]['id']+' data-coord_x="'+data['coord_x']+'" data-coord_y="'+data['coord_y']+'">'+order_list[k]['name']+'</option>'
            );
            //order.append($("<option/>", {
            //  value: order_list[k]['id'],
            //  text: order_list[k]['name'],
            //  coord_x: order_list[k]['coord_x'],
            //  coord_y: order_list[k]['coord_y']
            //}));
          }
        }

      });
      distributor.parents('.form-group').removeClass('hide');
      order.parents('.form-group').removeClass('hide');
    } else {
      distributor.find('option').remove();
      order.find('option').remove();
      distributor.parents('.form-group').addClass('hide');
      order.parents('.form-group').addClass('hide');
    }
  });
  // валидация формы редактирования задачи на проведение промо акции
  var d_t_p_u_form = $('#js-form-distributor-task-promo-update');
  d_t_p_u_form.validate({
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
      date: {
        required: true
      },
      coord_x: {
        required: true
      },
      coord_y: {
        required: true
      }
    }
  });
  d_t_p_u_form.find('#id_sale').change(function(){
    var distributor = d_t_p_u_form.find('#id_distributor');
    var order = d_t_p_u_form.find('#id_order');
    var url = $(this).parents('.form-group').data('url');
    if($(this).val()){
      $.ajax({
        type: "GET",
        url: url,
        data: {
          sale: $(this).val(),
          category: d_t_p_u_form.find('#id_category').val()
        }
      }).done(function (data) {
        if(data.error){
          $.notify(data.error, 'success');
        } else {
          var distributor_list = data.distributor_list;
          var order_list = data.order_list;
          distributor.find('option').remove();
          distributor.append($("<option value selected='selected'>---------</option>"));
          for (var i = 0; i < distributor_list.length; i++) {
            distributor.append($("<option/>", {
              value: distributor_list[i]['id'],
              text: distributor_list[i]['name']
            }));
          }
          order.find('option').remove();
          order.append($("<option value selected='selected'>---------</option>"));
          for (var k = 0; k < order_list.length; k++) {
            order.append(
              '<option value='+order_list[k]['id']+' data-coord_x="'+data['coord_x']+'" data-coord_y="'+data['coord_y']+'">'+order_list[k]['name']+'</option>'
            );
            //order.append($("<option/>", {
            //  value: order_list[k]['id'],
            //  text: order_list[k]['name']
            //}));
          }
        }
      });
    } else {
      distributor.find('option').remove();
      order.find('option').remove();
    }
  });
});
