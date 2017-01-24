/**
 * Created by alexy on 23.01.17.
 */
$(function() {
  $('#standContainer')
	    .bind("mousedown", function(e) {e.metaKey = false;})
	    .selectable();
  var minBlockHeight = 120;
  var minBlockWidth = 200;

  $('#js-combine-units').click(function(){
    var selected = $('.ui-selected');
    if (selected.length > 1) {
      var x_coords = [];
      var y_coords = [];
      var x1_coords = [];
      var y1_coords = [];
      var top1 = selected.first().position()['top'];
      var left1 = selected.first().position()['left'];
      var top2 = selected.last().position()['top'];
      var left2 = selected.last().position()['left'];
      var blockWidth = selected.last().outerWidth();
      var blockHeight = selected.last().outerHeight();
      var new_width = left2 - left1 + blockWidth;
      var new_height = top2 - top1 + blockHeight;
      var min_x, max_x, min_y, max_y;
      var s = 0, s1;
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

      if (s==s1) {
        selected.first().before(
          '<div class="block" style="top:'+ top1 +
          'px;left:' + left1 +
          'px;width:' + new_width +
          'px;height:' + new_height +
          'px;z-index:10;">' +
          'Новый блок</div>'
        );
        selected.remove();
      } else {
        alert('Нельзя объединить!');
      }
    } else {
      alert('Нужно выбрать больше одно элемента');
    }

  });
  $('#js-break-units').click(function(){
    var selected = $('.ui-selected');
    console.log('Выделено элементов: ' + selected.length);
  });
});