from django import template

register = template.Library()
"""
In this module we define various template filter that we can load through a particular tag and use in out html template.
"""
def cut(value, arg):
	"""
	Removes all values of arg from the given string.

	This filter would be used like this: {{ somevariable|cut:"arg" }}
	"""
	return value.replace(arg, '')

def lower(value):
	" Return value to lowercase "
	return value.lower()

"When the filters are written, you need to register them in the Library instance for them to be available."
register.filter('cut', cut)
register.filter('lower', lower)

"the other way to register it is using a decorator"

@register.filter(name='upper')
def upper(value):
	return value.upper()


"""
-----------------------------------------------------------------------------------------------------------------------------------------
In a file like this can also be registered custom tags!"""


def do_upper(parser, token):
	nodelist = parser.parse(('endupper',))
	parser.delete_first_token()
	return UpperNode(nodelist)

class UpperNode(template.Node):

	def __init__(self, nodelist):
		self.nodelist = nodelist

	def render(self, context):
		output = self.nodelist.render(context)
		return output.upper()

register.tag('upper', do_upper)