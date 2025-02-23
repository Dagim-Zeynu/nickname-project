from django import template

register = template.Library()

@register.filter
def reaction_count(nickname, reaction_type):
    return nickname.reactions.filter(reaction_type=reaction_type).count()
