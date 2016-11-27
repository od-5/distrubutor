# coding=utf-8
from django.conf import settings
from django.utils.http import urlquote
from core.geotagging import url_fix
import urllib
import urllib2


__author__ = 'alexy'


servicecodes={
    100: u"Сообщение принято к отправке. На следующих строчках вы найдете идентификаторы отправленных сообщений в том же порядке, в котором вы указали номера, на которых совершалась отправка.",
    200: u"Неправильный api_id",
    201: u"Не хватает средств на лицевом счету",
    202: u"Неправильно указан получатель",
    203: u"Нет текста сообщения",
    204: u"Имя отправителя не согласовано с администрацией",
    205: u"Сообщение слишком длинное (превышает 8 СМС)",
    206: u"Будет превышен или уже превышен дневной лимит на отправку сообщений",
    207: u"На этот номер (или один из номеров) нельзя отправлять сообщения, либо указано более 100 номеров в списке получателей",
    208: u"Параметр time указан неправильно",
    209: u"Вы добавили этот номер (или один из номеров) в стоп-лист",
    210: u"Используется GET, где необходимо использовать POST",
    211: u"Метод не найден",
    220: u"Сервис временно недоступен, попробуйте чуть позже.",
    300: u"Неправильный token (возможно истек срок действия, либо ваш IP изменился)",
    301: u"Неправильный пароль, либо пользователь не найден",
    302: u"Пользователь авторизован, но аккаунт не подтвержден (пользователь не ввел код, присланный в регистрационной смс)",
}


def send_sms(phone_number, message):
    api_key = settings.SMS_RU_API_KEY
    url = u'http://sms.ru/sms/send?%s'
    params = {
        'api_id': api_key,
        'to': phone_number,
        'text': message.encode('utf-8')
    }
    smsAPI = url % urllib.urlencode(params)
    # print smsAPI
    f = urllib2.urlopen(smsAPI)
    service_result = f.read().splitlines()
    # if service_result is not None:
    #     for i in service_result:
    #         print i
    return service_result
