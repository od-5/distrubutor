/**
 * Created by alexy on 28.05.15.
 */
$(function() {
  $.datepicker.setDefaults(
        $.extend($.datepicker.regional["ru"])
  );
  var client_search_form = $('#js-client-search-form');
  client_search_form.find("#id_date_start").datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  client_search_form.find("#id_date_end").datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  var sale_dash_form = $("#js-sale-dash-form");
  sale_dash_form.find("#id_date_start").datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  sale_dash_form.find("#id_date_end").datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  var sale_order_form = $("#js-form-sale-order");
  sale_order_form.find('#id_date_start').datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  sale_order_form.find('#id_date_end').datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  $('#js-form-sale-maket').find('#id_date').datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  var task_search_form = $('#js-form-task-search');
  task_search_form.find('#id_date_s').datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  task_search_form.find('#id_date_e').datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  $('#js-form-task-add').find('#id_date').datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  $('#js-form-task-update').find('#id_date').datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  $('#js-task-modal-add-form').find('#id_date').datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  $('#js-task-modal-update-form').find('#id_date').datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  $('#js-form-distributor-task').find('#id_date').datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  $('#js-form-distributor-task-add').find('#id_date').datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  $('#js-distributor-task-list-search-form').find('#id_date').datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  $('#js-form-moderator-update').find('#id_deny_date').datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  var manager_report_form = $('.js-manager-report-form');
  manager_report_form.find('#id_date_s').datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  manager_report_form.find('#id_date_e').datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });

});