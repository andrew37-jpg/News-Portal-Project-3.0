from django import template

register = template.Library()

@register.filter(name='Censor')
def Censor(value):
    Banned_List = ['idiot', 'stupid', 'donkey', 'Stupid']
    sentence = value.split()
    for i in Banned_List:
        for words in sentence:
            if i in words:
                pos = sentence.index(words)
                sentence.remove(words)
                sentence.insert(pos, '*' * len(i))
    return " ".join(sentence)

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
   d = context['request'].GET.copy()
   for k, v in kwargs.items():
       d[k] = v
   return d.urlencode()