# coding=utf-8
from django.views.generic.edit import FormMixin

__author__ = '2mitrij'


# TODO: внедрить миксин
class RedirectlessFormMixin(FormMixin):
    """
    Миксин реализует поведение формы при котором после успешной валидации формы не производится редиректа.
    P.S. Такое поведение противоречит общепринятой модели PRG(Post/Redirect/Get) приложений.
    """
    def form_valid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form))


# TODO: внедрить миксин
class SendUserToFormMixin(FormMixin):
    """
    Миксин добавляет текущего пользователя в аргументы инициализации формы.
    """
    def get_form_kwargs(self):
        kwargs = super(SendUserToFormMixin, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
