/**
 * Created by alexy on 23.01.17.
 */
$(function() {
  $('#standContainer')
	    .bind("mousedown", function(e) {e.metaKey = false;})
	    .selectable();
  var minBlockHeight = 120;
  var minBlockWidth = 200;
  function sortingCoords (a, b) {
      var az = Math.sqrt(a[0] * a[0] + a[1] * a[1]);
      var bz = Math.sqrt(b[0] * b[0] + b[1] * b[1]);
      if(az == bz) return 0;
      return (az < bz) ? -1 : 1;
  }
  $('#js-combine-units').click(function(){
    var selected = $('.ui-selected');
    if (selected.length > 1) {
      var error_flag = 0;
      var coords = [];
      var top1 = selected.first().position()['top'];
      var left1 = selected.first().position()['left'];
      var top2 = selected.last().position()['top'];
      var left2 = selected.last().position()['left'];
      //var blockWidth = selected.last().outerWidth();
      //var blockHeight = selected.last().outerHeight();
      //var width = left2 - left1 + blockWidth;
      //var height = top2 - top1 + blockHeight;
      var a = 0, b = 0, c = 0, d = 0;
      var left = 0, top = 0, width = 0, height = 0;
      selected.each(function(){
        left = $(this).position()['left'];
        top = $(this).position()['top'];
        width = $(this).outerWidth();
        height = $(this).outerHeight();
        a = top + left;
        b = top + (left + width);
        c = (top + height) + left;
        d = (top + height) + (left + width);
        coords.push([a, b, c, d]);
      });
      var coordsLength = coords.length;
      function equal_two_coord(arr1, arr2) {
        if (arr1.length == arr2.length) {
          console.log(1);
          return false;
        } else {
          console.log(2);
          return 'ok';
        }
      }
      for (var i = 0; i < coordsLength; i++){
        console.log(coords[i]);
        console.log(i, i+1);
      }
      equal_two_coord(coords[0], coords[1]);
      //console.log(coords.sort(sortingCoords));
      //var n = 0;
      //while (n < selected.length) {
      //  console.log(selected[n]);
      //  n++;
      //}
    } else {
      alert('Нужно выбрать больше одно элемента');
    }

  });
  $('#js-break-units').click(function(){
    var selected = $('.ui-selected');
    console.log('Выделено элементов: ' + selected.length);
  });
});