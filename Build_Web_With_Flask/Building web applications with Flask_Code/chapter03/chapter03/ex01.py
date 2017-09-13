# coding:utf-8

with open('parent.html', 'w') as file:
    file.write("""
{% block template %}parent.html{% endblock %}
===========
I am a powerful psychic and will tell you your past

{#- "past" is the block identifier #}
{% block past %}
You had pimples by the age of 12.
{%- endblock %}

Tremble before my power!!!
""".strip())

with open('child.html', 'w') as file:
    file.write("""
{% extends "parent.html" %}

{# overwriting the block called template from parent.html #}
{% block template %}child.html{% endblock %}

{#- overwriting the block called past from parent.html #}
{% block past %}
You've bought a ebook recently.
{%- endblock %}
""".strip())

from jinja2 import Environment, FileSystemLoader

env = Environment()
env.loader = FileSystemLoader('.')
tmpl = env.get_template('parent.html')
print tmpl.render()

print ""

tmpl = env.get_template('child.html')
print tmpl.render()
