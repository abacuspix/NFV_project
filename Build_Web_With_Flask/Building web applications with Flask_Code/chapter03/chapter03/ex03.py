# coding:utf-8

with open('formfield.html', 'w') as file:
    file.write('''
{% macro input(name, value='', label='') -%}
{% if label %}
<label for='{{ name }}'>{{ label }}</label>
{%- endif %}
<input id='{{ name }}' name='{{ name }}' value='{{ value }}'></input>
{%- endmacro %}
'''.strip())

with open('index.html', 'w') as file:
    file.write('''
{% from 'formfield.html' import input %}
<form method='get' action='.'>
{{ input('name', label='Name:') }}
<input type='submit' value='Send'></input>
</form>
'''.strip())

from jinja2 import Environment, FileSystemLoader

env = Environment()
env.loader = FileSystemLoader('.')
print env.get_template('index.html').render()
