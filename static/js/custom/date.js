/**
 * Created by alexy on 28.05.15.
 */
$(function() {
  $.datepicker.setDefaults(
        $.extend($.datepicker.regional["ru"])
  );
  var moderator_order_search_form = $('#js-moderator-order-search-form');
  moderator_order_search_form.find("#id_date_start").datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  moderator_order_search_form.find("#id_date_end").datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
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
  $('#js-form-distributor-task-update').find('#id_date').datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  $('#js-form-distributor-task-promo-add').find('#id_date').datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  $('#js-form-distributor-task-promo-update').find('#id_date').datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  $('#js-form-distributor-task-quest-add').find('#id_date').datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  $('#js-form-distributor-task-quest-update').find('#id_date').datepicker({
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
  var ticket_filter_form = $('.js-ticket-filter-form');
  ticket_filter_form.find('#id_date_s').datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  ticket_filter_form.find('#id_date_e').datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  var distributor_report_form = $('.js-distributor-report-form');
  distributor_report_form.find('#id_date_s').datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  distributor_report_form.find('#id_date_e').datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });

  var commissionorder_search_form = $('#js-commissionorder-search-form');
  commissionorder_search_form.find('#id_date_s').datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  commissionorder_search_form.find('#id_date_e').datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  var stand_add_form = $('#js-form-stand-add');
  stand_add_form.find('#id_date_start').datepicker({
    defaultDate: 0,
    dateFormat: "dd.mm.yy"
  });
  stand_add_form.find('#id_date_end').datepicker({
    defaultDate: 7,
    dateFormat: "dd.mm.yy"
  });
  var stand_update_form = $('#js-form-stand-update');
  stand_update_form.find('#id_date_start').datepicker({
    defaultDate: 0,
    dateFormat: "dd.mm.yy"
  });
  stand_update_form.find('#id_date_end').datepicker({
    defaultDate: 7,
    dateFormat: "dd.mm.yy"
  });
  var stand_search_form = $('#js-stand-search-form');
  stand_search_form.find('#id_date_start').datepicker({
    defaultDate: 0,
    dateFormat: "dd.mm.yy"
  });
  stand_search_form.find('#id_date_end').datepicker({
    defaultDate: 7,
    dateFormat: "dd.mm.yy"
  });



});
