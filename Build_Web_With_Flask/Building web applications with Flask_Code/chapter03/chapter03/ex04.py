# coding:utf-8

# Write the macro template
with open('formfield.html', 'w', encoding='utf-8') as file:
    file.write('''
{% macro input(name, **kwargs) -%}
<input id='{{ name }}' name='{{ name }}' {% for k, v in kwargs.items() -%}{{ k }}='{{ v }}' {% endfor %}></input>
{%- endmacro %}
'''.strip())

# Write the main template
with open('index.html', 'w', encoding='utf-8') as file:
    file.write('''
{% from 'formfield.html' import input %}
<form method='get' action='.'>
{{ input('name', type='text') }}
{{ input('passwd', type='password') }}
<input type='submit' value='Send'></input>
</form>
'''.strip())

from jinja2 import Environment, FileSystemLoader

# Set up the Jinja2 environment
env = Environment(loader=FileSystemLoader('.'))

# Render the index template
output = env.get_template('index.html').render()
print(output)
