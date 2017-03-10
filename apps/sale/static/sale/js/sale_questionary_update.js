$(function() {
  function bindAnswerFormset($el) {
    $el.formset_improved({
      animateForms: true,
      form: '[data-formset_answer-form]',
      emptyForm: '[data-formset_answer-empty-form]',
      body: '[data-formset_answer-body]',
      add: '[data-formset_answer-add]',
      deleteButton: '[data-formset_answer-delete-button]',
      empty_prefix: '__answer_prefix__'
    });
  };

  $('#js-sale-questionary-question-formset > div[data-formset-body]').on('formAdded', function(event) {
      var $new_form = $(event.target);
      bindAnswerFormset($new_form.find('.js-sale-questionary-answer-formset'));

      var question_type = $new_form.find('input[type=radio]:checked').val();
      if (question_type != 2) {
        $new_form.find('.js-sale-questionary-answer-formset').addClass('hidden');
      }

      $new_form.change(function(event) {
        var $form = $(event.currentTarget);
            $el = $(event.target);

        if ($form.is('[data-formset-form]') && $el.is('input[type=radio]')) {
          if ($el.val() == 1) {
            var answer_formset = $form.find('.js-sale-questionary-answer-formset').formset_improved('getOrCreate');
            answer_formset.$forms().each(function() {
              $(this).find(answer_formset.opts.deleteButton).trigger('click');
            });
            $form.find('.js-sale-questionary-answer-formset').addClass('hidden');
          }
          else if ($el.val() == 2) {
            $form.find('.js-sale-questionary-answer-formset').removeClass('hidden');
          }
        }
      });
  });

  $('#js-sale-questionary-question-formset').formset_improved({
    animateForms: true
  });
});
