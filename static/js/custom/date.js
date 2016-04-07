/**
 * Created by alexy on 28.05.15.
 */
$(function() {
  $.datepicker.setDefaults(
        $.extend($.datepicker.regional["ru"])
  );
  var sale_order_dorm = $("#js-form-sale-order");
  sale_order_dorm.find('#id_date_start').datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  sale_order_dorm.find('#id_date_end').datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  $('#js-form-sale-maket').find('#id_date').datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });


});