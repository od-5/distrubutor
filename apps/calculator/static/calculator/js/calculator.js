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


});