# coding:utf-8

# Writing parent template
with open('parent.html', 'w', encoding='utf-8') as file:
    file.write("""
{% block template %}parent.html{% endblock %}
===========
I am a powerful psychic and will tell you your past:

{# "past" is the block identifier #}
{% block past %}
You had pimples by the age of 12.
{% endblock %}

Tremble before my power!!!
""".strip())

# Writing child template
with open('child.html', 'w', encoding='utf-8') as file:
    file.write("""
{% extends "parent.html" %}

{# Overwriting the block called template from parent.html #}
{% block template %}child.html{% endblock %}

{# Overwriting the block called past from parent.html #}
{% block past %}
You've bought an ebook recently.
{% endblock %}
""".strip())

from jinja2 import Environment, FileSystemLoader

# Setting up Jinja2 Environment
env = Environment(loader=FileSystemLoader('.'))

# Rendering parent template
tmpl = env.get_template('parent.html')
print(tmpl.render())  # Use print() for Python 3 compatibility

print("\n" + "="*20 + "\n")

# Rendering child template
tmpl = env.get_template('child.html')
print(tmpl.render())
