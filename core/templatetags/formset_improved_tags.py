# coding=utf-8
"""
Часть батарейки.
Взято здесь: https://github.com/pretix/django-formset-js/blob/master/djangoformsetjs/templatetags/formset_tags.py.
"""
# TODO: по хорошему надо подключить батарейку, пока мешает конфликт jQuery плагинов
from __future__ import unicode_literals
from django.template import Library, Node

register = Library()


class EscapeScriptNode(Node):
    TAG_NAME = 'escapescript'

    def __init__(self, nodelist):
        super(EscapeScriptNode, self).__init__()
        self.nodelist = nodelist

    def render(self, context):
        out = self.nodelist.render(context)
        escaped_out = out.replace('</script>', '<\\/script>')
        return escaped_out


@register.tag(EscapeScriptNode.TAG_NAME)
def media(parser, token):
    nodelist = parser.parse(('end' + EscapeScriptNode.TAG_NAME,))
    parser.delete_first_token()
    return EscapeScriptNode(nodelist)
