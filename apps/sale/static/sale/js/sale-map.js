/**
 * Created by alexy on 02.11.16.
 */
ymaps.ready(init);
function init() {
  var map_id = $('#map');
  var url = map_id.data('url');
  var category = $('#id_category').val();
  var task = $('#id_task').val();
  var order = $('#id_order').val();
  var date_start = $('#id_date_start').val();
  var date_end = $('#id_date_end').val();
  var data_list = '';
  var all_address_list = '';
  var center = '';
  $('#js-photo-map-button').click(function(){
    $('#map').empty();
    $.ajax({
      type: "POST",
      async: false,
      url: url,
      data: {
        task: task,
        category: category,
        order: order,
        date_start: date_start,
        date_end: date_end
      }
    }).done(function (data) {
      center = data.center;
      if (data.all_address_list.length){
        all_address_list = data.all_address_list;
      } else {
        if (data.coord_list.length){
          data_list = data.coord_list;
        } else {
          if (data.address_list.length) {
            data_list = data.address_list;
          }
        }
      }
    });
    var myMap = new ymaps.Map("map", {
        center: center,
        zoom: 13
      }, {
        searchControlProvider: 'yandex#search'
    });
    // отображение карты, если задача не выбрана
    // отображение карты при выборе задачи
    if (all_address_list.length) {
      console.log('Полный список точек');
      for(var i = 0; i < all_address_list.length; i++) {
        myMap.geoObjects.add(
              new ymaps.Placemark([all_address_list[i]['coord_x'], all_address_list[i]['coord_y']], {
              balloonContent: all_address_list[i]['name'],
              hintContent: all_address_list[i]['name']
              })
          );
      }
    // function outputItem(item, i, all_address_list)
    // all_address_list.forEach(outputItem);
    } else {
      if (data_list.length > 1){
        console.log('Маршрут');
        ymaps.route(
          data_list
        ).then(function (route) {
         //route.options.set('routingMode', 'pedestrian');
          myMap.geoObjects.add(route);
          var points = route.getWayPoints();
          points.options.set('preset', 'islands#redStretchyIcon');
        }, function (error) {
          console.log('Возникла ошибка: ' + error.message);
        });
      } else {
        if (data_list.length == 1){
        console.log('В маршруте всего одна точка!');
        myPlacemark = new ymaps.Placemark(myMap.getCenter(), {
                hintContent: data_list[0],
                balloonContent: data_list[0]
            });
        myMap.geoObjects.add(myPlacemark);
        } else {
          console.log('Точек нет!');
        }
      }
    }
  });
}