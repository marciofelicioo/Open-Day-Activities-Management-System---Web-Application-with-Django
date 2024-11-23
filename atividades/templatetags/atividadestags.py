from django import template
from django.core.exceptions import ObjectDoesNotExist
import json
from django.urls.base import reverse
from django.utils.safestring import mark_safe
from atividades.models import Sessao

register = template.Library()

@register.filter
def field_data(value):
    classes = 'class="' + str(value.field.widget.attrs.get('class')) + '"'
    result = str(classes)
    if value.name == 'horarioid':
        result += ' onchange="updateSchedules(\'' + str(value.auto_id) + '\')"'
    return result


@register.simple_tag
def has_conflict(value,activity_id):
    for conf in value:
        if conf.atividade1.atividadeid.id == activity_id:
            return mark_safe("<a type=\"button\" onclick=\"alert.render(\'A Atividade tem conflitos, tem a certeza que desenja proceder?\'," + "/atividades/validaratividade/"+ str(activity_id) +'/'+'0' + ");\"  class=\" button is-success\" style=\"margin-right: 10px;\" ><span class=\"icon is-small\"><i class=\"mdi mdi-check\"></i></span><span>Aceitar</span></a>")
    return mark_safe("<a type=\"button\" href=\" " + "/atividades/validaratividade/"+ str(activity_id) +'/'+'0' + "\" class=\" button is-success\" style=\"margin-right: 10px;\" ><span class=\"icon is-small\"><i class=\"mdi mdi-check\"></i></span><span>Aceitar</span></a>")

@register.filter
def colab_list(value):
    if len(value) == 0:
        return "N/A"
    else:
        str_names = ""
        none= []
        for colab in value :
            if colab is not None:
                str_names+=str(colab.full_name) +" "+ ","+ " "
        if str_names == "":
            return "N/A"
        return str_names[:-2]

@register.filter
def conflict_list(value):
    if len(value) != 0:
        return "Sem Colaboradores"
    else:
        str_names = ""
        for colab in value :
            if colab is not None:
                str_names+=str(colab.full_name) +','
        return str_names[:-1]


@register.filter
def material_none(value):
    if value is None:
        return "N/A"
    else:
        return value

@register.filter
def inscritos(value):
    inscritos= value.atividadeid.participantesmaximo- value.vagas
    return inscritos
