# coding:utf-8
with open('base.txt', 'w') as file:
    file.write("""
{{ myvar }}
You wanna hear a dirty joke?
{% include 'joke.txt' %}
""".strip())
with open('joke.txt', 'w') as file:
    file.write("""
A boy fell in a mud puddle. {{ myvar }} 
""".strip())

from jinja2 import Environment, FileSystemLoader

env = Environment()
# tell the environment how to load templates
env.loader = FileSystemLoader('.')
print env.get_template('base.txt').render(myvar='Ha ha!')
