/**
 * Created by alexy on 23.01.17.
 */
$(function() {
  //$('#standContainer')
  //  .bind("mousedown", function(e) {e.metaKey = true;})
  //  .selectable();
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
    console.log(selected.length);
    if (selected.length > 1) {
      var error_flag = 0;
      var top1 = selected.first().position()['top'];
      var left1 = selected.first().position()['left'];
      var top2 = selected.last().position()['top'];
      var left2 = selected.last().position()['left'];
      var blockWidth = selected.last().outerWidth();
      var blockHeight = selected.last().outerHeight();
      var width = left2 - left1 + blockWidth;
      var height = top2 - top1 + blockHeight;
      var coords = [];
      //selected.each(function(){
      //  coords.push([$(this).position()['left'], $(this).position()['top']]);
      //});
      //console.log(coords);
      //console.log(coords.sort(sortingCoords));
      if (width < 200){
        console.log('так нельзя выбирать!');
        error_flag = 1;
      }
      if (height < 120){
        error_flag = 1;
      }
      console.log('top1='+top1+'left1='+left1+'top2='+top2+'left2='+left2+'width='+width+'height='+height);
      console.log(selected.last());
      if (error_flag == 0) {
        //вставить перед выделенными блоками новый
        selected.first().before(
          '<div class="block" style="top:'+ top1 +
          'px;left:' + left1 +
          'px;width:' + width +
          'px;height:' + height +
          'px;z-index:10;">' +
          'Новый блок</div>'
        );
        //удалить выделенные блоки
        selected.remove();
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