# coding:utf-8

# Write the macro template
with open('formfield.html', 'w', encoding='utf-8') as file:
    file.write('''
{% macro input(name, value='', label='') -%}
{% if label %}
<label for='{{ name }}'>{{ label }}</label>
{%- endif %}
<input id='{{ name }}' name='{{ name }}' value='{{ value }}'></input>
{%- endmacro %}
'''.strip())

# Write the main template
with open('index.html', 'w', encoding='utf-8') as file:
    file.write('''
{% from 'formfield.html' import input %}
<form method='get' action='.'>
{{ input('name', label='Name:') }}
<input type='submit' value='Send'></input>
</form>
'''.strip())

from jinja2 import Environment, FileSystemLoader

# Set up the Jinja2 environment
env = Environment(loader=FileSystemLoader('.'))

# Render the index template
output = env.get_template('index.html').render()
print(output)
