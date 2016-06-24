/**
 * Created by alexy on 24.06.16.
 */
$(function() {
  $('#js-show-menu').click(function(){
    $('.navbar').slideToggle();
  });

  $('#js-show-search').click(function(){
    $('.form-search').slideToggle();
    $(this).find('.glyphicon-chevron-down').toggleClass('hide');
    $(this).find('.glyphicon-chevron-up').toggleClass('hide');
  });
  var sale_photo_search_form = $('#js-sale-photo-search-form');
  sale_photo_search_form.find("#id_date_start").datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
  sale_photo_search_form.find("#id_date_end").datepicker({
    defaultDate: 1,
    dateFormat: "dd.mm.yy"
  });
});