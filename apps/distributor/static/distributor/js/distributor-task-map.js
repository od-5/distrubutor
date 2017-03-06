/**
 * Created by alexy on 03.03.17.
 */
ymaps.ready(init);

function init() {
  // если координаты центра заданы - центрируем по ним карту
  var coord_x = $('#id_coord_x').val();
  var coord_y = $('#id_coord_y').val();
  var center;
  if (coord_x && coord_y) {
    center = [coord_x, coord_y];
  } else {
    center = [55.753994, 37.622093]
  }
  //alert(center);
  var myPlacemark,
      myMap = new ymaps.Map('map', {
          center: center,
          zoom: 9
      }, {
          searchControlProvider: 'yandex#search'
      });
  if (coord_x && coord_y) {
    myPlacemark = createPlacemark(center);
    myMap.geoObjects.add(myPlacemark);
    getAddress(myPlacemark.geometry.getCoordinates());
  }
  // Слушаем клик на карте.
  myMap.events.add('click', function (e) {
    var coords = e.get('coords');
    // записываем полученные координаты

    $('#id_coord_x').val(coords[0].toFixed(6));
    $('#id_coord_y').val(coords[1].toFixed(6));
    // Если метка уже создана – просто передвигаем ее.
    if (myPlacemark) {
      myPlacemark.geometry.setCoordinates(coords);
    }
    // Если нет – создаем.
    else {
      myPlacemark = createPlacemark(coords);
      myMap.geoObjects.add(myPlacemark);
      // Слушаем событие окончания перетаскивания на метке.
      myPlacemark.events.add('dragend', function () {
          getAddress(myPlacemark.geometry.getCoordinates());
      });
    }
    getAddress(coords);
  });

  // Создание метки.
  function createPlacemark(coords) {
    return new ymaps.Placemark(coords, {
      iconCaption: 'поиск...'
    }, {
      preset: 'islands#violetDotIconWithCaption',
      draggable: true
    });
  }

  // Определяем адрес по координатам (обратное геокодирование).
  function getAddress(coords) {
    myPlacemark.properties.set('iconCaption', 'поиск...');
    ymaps.geocode(coords).then(function (res) {
      var firstGeoObject = res.geoObjects.get(0);

      myPlacemark.properties
          .set({
              iconCaption: firstGeoObject.properties.get('name'),
              balloonContent: firstGeoObject.properties.get('text')
          });
    });
  }
  // перемещаем центр карты при выборе заказа
  $('form').on('change', '#id_order', function(){
    if ($(this).val()){
      $('#map-container').removeClass('hide');
      myMap.setCenter([$('#id_order option:selected').data('coord_y'), $('#id_order option:selected').data('coord_x')], 11, {
        checkZoomRange: true
      });
    } else {
      $('#map-container').addClass('hide');
    }
  });
}
