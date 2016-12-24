/**
 * Created by alexy on 24.02.16.
 */
$(function() {

  //  Добавление задачи для монтажника по клиенту
  var calc_form = $('#js-calculator-form');
  calc_form.validate({
    rules: {
      country: {
        required: true
      },
      city: {
        required: true
      },
      moderator: {
        required: true
      },
      type: {
        required: true
      },
      count: {
        required: true
      }
    }
  });

  // Получение списка городов по выбранной стране
  calc_form.find('#id_country').change(function() {
    var country = $(this).val();
    var url = $(this).data('url');
    if (country == '') {
      calc_form.find('#id_city').find('option').remove();
      calc_form.find('#id_city').append($("<option value selected='selected'>--------</option>"));
      calc_form.find('#id_moderator').find('option').remove();
      calc_form.find('#id_moderator').append($("<option value selected='selected'>--------</option>"));
      calc_form.find('#id_type').find('option').remove();
      calc_form.find('#id_type').append($("<option value selected='selected'>--------</option>"));
    } else {
      calc_form.find('#id_city').removeClass('hide');
      $.ajax({
        type: "GET",
        url: url,
        data: {
          country: country
        }
      }).done(function (data) {
        // заполняем список городов
        var city_selector = calc_form.find('#id_city');
        city_selector.find('option').remove();
        city_selector.append($("<option value selected='selected'>---- Выберите город ----</option>"));
        for (var i = 0; i < data.city_list.length; i++) {
          city_selector.append($("<option/>", {
            value: data.city_list[i]['id'],
            text: data.city_list[i]['name']
          }));
        }
        // обнуляем список модераторов и видов деятельности
        calc_form.find('#id_moderator').find('option').remove();
        calc_form.find('#id_moderator').append($("<option value selected='selected'>--------</option>"));
        calc_form.find('#id_type').find('option').remove();
        calc_form.find('#id_type').append($("<option value selected='selected'>--------</option>"));
      });
    }
  });

  // Получение списка исполнителей по выбранному городу
  calc_form.find('#id_city').change(function() {
    var city = $(this).val();
    var url = $(this).data('url');
    if (city == '') {
      calc_form.find('#id_moderator').find('option').remove();
      calc_form.find('#id_moderator').append($("<option value selected='selected'>--------</option>"));
      calc_form.find('#id_type').find('option').remove();
      calc_form.find('#id_type').append($("<option value selected='selected'>--------</option>"));
    } else {
      $.ajax({
        type: "GET",
        url: url,
        data: {
          city: city
        }
      }).done(function (data) {
        // заполняем список исполнителей
        var moderator_selector = calc_form.find('#id_moderator');
        moderator_selector.find('option').remove();
        moderator_selector.append($("<option value selected='selected'>---- Выберите исполнителя ----</option>"));
        for (var i = 0; i < data.moderator_list.length; i++) {
          moderator_selector.append($("<option/>", {
            value: data.moderator_list[i]['id'],
            text: data.moderator_list[i]['name']
          }));
        }
        // обнуляем список видов деятельности
        calc_form.find('#id_type').find('option').remove();
        calc_form.find('#id_type').append($("<option value selected='selected'>--------</option>"));
      });
    }
  });

  // Получение списка видов деятельности по выбранному исполнителю
  calc_form.find('#id_moderator').change(function() {
    var moderator = $(this).val();
    var url = $(this).data('url');
    if (moderator == '') {
      calc_form.find('#id_type').find('option').remove();
      calc_form.find('#id_type').append($("<option value selected='selected'>--------</option>"));
    } else {
      $.ajax({
        type: "GET",
        url: url,
        data: {
          moderator: moderator
        }
      }).done(function (data) {
        // заполняем список видов деятельности
        var type_selector = calc_form.find('#id_type');
        type_selector.find('option').remove();
        type_selector.append($("<option value selected='selected'>---- Выберите вид деятельности ----</option>"));
        for (var i = 0; i < data.action_list.length; i++) {
          type_selector.append($("<option/>", {
            value: data.action_list[i]['id'],
            text: data.action_list[i]['name']
          }));
        };
      });
    }
  });

  // Расчет цены по submit формы
  calc_form.submit(function (e) {
    e.preventDefault();

    if (!calc_form.valid()) {
      return true;
    }

    var type = $('#id_type').val(),
        count = $('#id_count').val(),
        url = $('#id_type').data('url');

    count = parseInt(count);

    if (count < 0) {
      count = 0
    }

    $('#id_count').val(count);

    // Запрашиваем стоимость по виду деятельности
    $.ajax({
      type: "GET",
      url: url,
      data: {
        action: type
      }
    }).done(function (data) {
      var result_cost = count * data.cost;
      $('#js-result-cost').text(result_cost);
    });
  });
});