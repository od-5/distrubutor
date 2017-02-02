/**
 * Created by alexy on 23.01.17.
 */
$(function() {
  $('#standContainer')
      .bind("mousedown", function(e) {e.metaKey = false;})
      .selectable({
        selecting: function (event, ui) {
          $('.ui-selected').removeClass('ui-selected');
        }
      });
  $('#topStandContainer')
      .bind("mousedown", function(e) {e.metaKey = false;})
      .selectable({
        selecting: function (event, ui) {
          $('.ui-selected').removeClass('ui-selected');
        }
      });
  $('#standContainer1')
      .bind("mousedown", function(e) {e.metaKey = false;})
      .selectable({
        selecting: function (event, ui) {
          $('.ui-selected').removeClass('ui-selected');
        }
      });
  $('#topStandContainer1')
      .bind("mousedown", function(e) {e.metaKey = false;})
      .selectable({
        selecting: function (event, ui) {
          $('.ui-selected').removeClass('ui-selected');
        }
      });
  $('.js-check-units').click(function(){
    var check = 0;
    var selected = $('.block.ui-selected');

  });
  $('.js-combine-units').click(function(){
    //fixme: сделать проверку - менеджер не может объединять блоки, которые создавал не он
    var selected = $('.block.ui-selected');
    if (selected.length > 1) {
      var x_coords = [],
          y_coords = [],
          x1_coords = [],
          y1_coords = [];
      var min_x, max_x, min_y, max_y;
      var s = 0, s1 = 0;
      var top, left, width, height;
      selected.each(function(){
        left = $(this).position()['left'];
        top = $(this).position()['top'];
        width = $(this).outerWidth();
        height = $(this).outerHeight();
        y_coords.push($(this).position()['top']);
        y1_coords.push($(this).position()['top']+height);
        x_coords.push($(this).position()['left']);
        x1_coords.push($(this).position()['left']+width);
        s += width*height;
      });
      min_x = Math.min.apply(null, x_coords);
      max_x = Math.max.apply(null, x1_coords);
      min_y = Math.min.apply(null, y_coords);
      max_y = Math.max.apply(null, y1_coords);
      s1 = (max_y - min_y) * (max_x - min_x);
      var new_width = max_x - min_x;
      var new_height = max_y - min_y;
      if (s==s1) {
        selected.first().before(
          '<div class="block" style="top:'+ min_y +
          'px;left:' + min_x +
          'px;width:' + new_width +
          'px;height:' + new_height +
          'px;z-index:10;">' +
          '<textarea class="stand-input" placeholder="Название клиента"></textarea>' +
          '<div class="js-standitem-manager">Менеджер:</div>'+
          '<div>Дата создания: <span class="js-standitem-created"></span></div></div>'
        );
        selected.remove();
      } else {
        // fixme: сделать выводод предупреждения на странице не через alert
        alert('Нельзя объединить!');
      }
    } else {
      // fixme: сделать выводод предупреждения на странице не через alert
      alert('Нужно выбрать больше одно элемента');
    }

  });
  $('.js-break-units').click(function(){
    //fixme: сделать проверку - менеджер не может разбивать блоки, которые создавал не он
    var selected = $('.block.ui-selected');
    if (selected.length == 1) {
      var minBlockHeight = selected.first().parent().data('min-height');
      var minBlockWidth = selected.first().parent().data('min-width');
      var topFirst = selected.first().position()['top'];
      var leftFirst = selected.first().position()['left'];
      var blockWidth = selected.last().outerWidth();
      var blockHeight = selected.last().outerHeight();
      var x_factor = blockWidth / minBlockWidth;
      var y_factor = blockHeight / minBlockHeight;
      var newBlockCount = x_factor*y_factor;
      if (newBlockCount > 1) {
        var a = 1;
        var new_top = topFirst;
        while (a <=y_factor) {
          var b = 1;
          var new_left = leftFirst;
          while (b <= x_factor) {
            selected.first().before(
              '<div class="block" style="top:'+ new_top +
              'px;left:' + new_left +
              'px;width:' + minBlockWidth +
              'px;height:' + minBlockHeight +
              'px;z-index:10;">' +
              '<textarea class="stand-input" placeholder="Название клиента"></textarea>' +
              '<div class="js-standitem-manager">Менеджер:</div>'+
              '<div>Дата создания: <span class="js-standitem-created"></span></div></div>'
            );
            new_left += minBlockWidth;
            b++;
          }
          new_top += minBlockHeight;
          a++;
        }
        selected.remove();
      } else {
        alert('Нельзя разбить на более мелкие блоки');
      }
    } else {
      alert('Можно разбить только один большой блок на несколько!')
    }
  });
  $('#js-stand-save').click(function(){
    var selected = $('.block');
    var top, width, left, height, side, position, client, manager, url, created, csrftoken, stand;
    csrftoken = $('input[name=csrfmiddlewaretoken]').val();
    $.ajax({
      type: "POST",
      async: false,
      data: {
        stand: selected.first().parents('.stand-container').data('stand'),
        csrfmiddlewaretoken: csrftoken
      },
      url: selected.first().parents('.stand-container').data('delete-url')
    });
    selected.each(function(){
      left = $(this).position()['left'];
      top = $(this).position()['top'];
      width = $(this).outerWidth();
      height = $(this).outerHeight();
      client = $(this).find('textarea').val();
      position = $(this).parents('div').data('position');
      side = $(this).parents('.stand-container').data('side');
      url = $(this).parents('.stand-container').data('url');
      stand = $(this).parents('.stand-container').data('stand');
      manager = $(this).find('.js-standitem-manager').attr('data-manager');
      created = $(this).find('.js-standitem-created').text();
      $.ajax({
        type: "POST",
        data: {
          stand: stand,
          width: width,
          height: height,
          top: top,
          left: left,
          client: client,
          side: side,
          position: position,
          manager: manager,
          created: created,
          csrfmiddlewaretoken: csrftoken
        },
        url: url
      });
      $('#js-form-stand-update').submit();
    });
  });
  //var today = new Date();
  //console.log(today.toLocaleDateString());
  $('.stand-container').on('change', '.stand-input', function(){
  // при изменении названия клиента устанавливаем текущую даты
    var today = new Date();
    $(this).parents('.block').find('.js-standitem-created').text(today.toLocaleDateString());
    var save_button = $('#js-stand-save');
    var current_manager = save_button.data('manager');
    var current_manager_name = save_button.data('name');

    if (current_manager) {
      console.log(current_manager);
      console.log(current_manager_name);
      $(this).parents('.block').find('.js-standitem-manager').text(current_manager_name);
      $(this).parents('.block').find('.js-standitem-manager').attr('data-manager', current_manager);
    }
  // если пользователь является менеджером, то прикрепляем его к блоку
  });
});