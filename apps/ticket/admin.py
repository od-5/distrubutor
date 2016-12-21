# coding=utf-8
from django.contrib import admin
from .models import Ticket
from django.forms import ModelForm
from suit.widgets import EnclosedInput, AutosizedTextarea


class TicketAdminForm(ModelForm):
    class Meta:
        widgets = {
            'comment': AutosizedTextarea,
        }


class TicketAdmin(admin.ModelAdmin):
    list_display = ('city', 'moderator', 'name', 'mail', 'phone', 'type', 'agency_manager', 'comment', 'created')
    list_filter = ['city', 'moderator', 'created', 'type', 'agency_manager', 'created']
    search_fields = ['mail', 'phone']
    date_hierarchy = 'created'
    readonly_fields = ('city', 'moderator')
    fields = ('city', 'moderator', 'name', 'mail', 'phone', 'agency_manager', 'type', 'comment')
    form = TicketAdminForm

    def get_queryset(self, request):
        qs = Ticket.objects.filter(type=0, moderator__ticket_forward=True, agency_manager__isnull=True)
        return qs


class Sale(Ticket):
    class Meta:
        proxy = True
        verbose_name = u'Продажа'
        verbose_name_plural = u'Продажи'


class SaleAdminForm(ModelForm):
    class Meta:
        widgets = {
            'price': EnclosedInput(append=u'руб.'),
            'comment': AutosizedTextarea,
        }


class SaleAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        user = request.user
        if user.is_superuser:
            return self.model.objects.filter(type=3)
        else:
            return self.model.objects.filter(agency_manager=user, type=3)

    def has_add_permission(self, request, obj=None):
        return False

    list_display = ('city', 'moderator', 'name', 'mail', 'phone', 'price', 'comment',)
    list_filter = ['city', 'moderator', ]
    search_fields = ['mail', ]
    date_hierarchy = 'created'
    readonly_fields = ('city', 'moderator')
    fields = ('city', 'moderator', 'name', 'mail', 'phone', 'agency_manager', 'type', 'comment')
    form = SaleAdminForm


class ManagerTicket(Ticket):
    class Meta:
        proxy = True
        verbose_name = u'Заявка в обработке'
        verbose_name_plural = u'Заявки в обработке'


class ManagerTicketForm(ModelForm):
    class Meta:
        widgets = {
            'comment': AutosizedTextarea,
        }


class ManagerTicketAdmin(admin.ModelAdmin):

    list_display = ('city', 'moderator', 'name', 'mail', 'phone', 'type', 'comment', 'created')
    list_filter = ['city', 'moderator', 'created', 'type', 'agency_manager', 'created']
    search_fields = ['mail', 'phone']
    date_hierarchy = 'created'
    readonly_fields = ('city', 'moderator')
    fields = ('city', 'moderator', 'name', 'mail', 'phone', 'agency_manager', 'type', 'comment')
    form = TicketAdminForm

    def get_queryset(self, request):
        qs = Ticket.objects.filter(agency_manager=request.user, type__in=[0, 1, 2])
        return qs


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(ManagerTicket, ManagerTicketAdmin)
