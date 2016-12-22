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
    var ajax_url = $(this).data('ajax-url');
    console.log(ajax_url);
    if (country == '') {
      calc_form.find('#id_city').addClass('hide');
      calc_form.find('#id_moderator').addClass('hide');
      calc_form.find('#id_type').addClass('hide');
    } else {
      calc_form.find('#id_city').removeClass('hide');
      $.ajax({
        type: "GET",
        url: ajax_url,
        data: {
          country: country
        }
      }).done(function (data) {
        // заполняем список городов
        console.log(data.city_list);
        var city_selector = calc_form.find('#id_city');
        city_selector.find('option').remove();
        city_selector.append($("<option value selected='selected'>--------</option>"));
        for (var i = 0; i < data.city_list.length; i++) {
          city_selector.append($("<option/>", {
            value: data.city_selector[i]['id'],
            text: data.city_selector[i]['name']
          }));
        }
        // обнуляем список модераторов и видов деятельности
        calc_form.find('#id_moderator').find('option').remove();
        calc_form.find('#id_type').find('option').remove();
      });
    }
  });


});