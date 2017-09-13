# coding:utf-8

with open('formfield.html', 'w') as file:
    file.write('''
{% macro input(name) -%}
<input id='{{ name }}' name='{{ name }}' {% for k,v in kwargs.items() -%}{{ k }}='{{ v }}' {% endfor %}></input>
{%- endmacro %}
'''.strip())

with open('index.html', 'w') as file:
    file.write('''
{% from 'formfield.html' import input %}
<form method='get' action='.'>
{{ input('name', type='text') }}
{{ input('passwd', type='password') }}
<input type='submit' value='Send'></input>
</form>
'''.strip())

from jinja2 import Environment, FileSystemLoader

env = Environment()
env.loader = FileSystemLoader('.')
print env.get_template('index.html').render()