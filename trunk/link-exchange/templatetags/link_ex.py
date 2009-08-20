from django import template
from link_exchange.models import Link
from django.template import get_library
    
register = template.Library()
 
       
@register.simple_tag
def link(link_name):
    """
    tag usage {%link "name"%}
    """
    l = Link.objects.get(name=link_name)
    if l is not None and l.active:
        if l.campaign.css_class.strip() <> "":
            css_class = u"""class="%s" """ % l.campaign.css_class.strip()
        else:
            css_class = u""
        if l.campaign.more_attribute.strip() <> "":
            more_attribute = u""" %s""" % l.campaign.more_attribute.strip()
        else:
            more_attribute = u""
        if l.campaign.target.strip() <> "":
            target = u""" target="%s" """ % l.campaign.target.strip()
        else:
            target = u""            
        return l.text % (u"""<a %s%s%s href="%s">%s</a>""" % (css_class, more_attribute, target, \
                                                              l.external_url, l.anchor))
    else:
        return u''
    
@register.tag(name="evaluate")
def do_evaluate(parser, token):
    """
    tag usage {%evaluate object.textfield%}
    """
    try:
        tag_name, variable = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]
    return EvaluateNode(variable)

class EvaluateNode(template.Node):
    def __init__(self, variable):
        self.variable = template.Variable(variable)
   
    def render(self, context):
        try:
            content = self.variable.resolve(context)
            t = template.Template("{%load link_ex%}" + content)
            return t.render(context)
        except template.VariableDoesNotExist, template.TemplateSyntaxError:
            return 'Error rendering', self.variable
            

