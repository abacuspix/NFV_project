# coding:utf-8
# Writing the base template
with open('base.txt', 'w', encoding='utf-8') as file:
    file.write("""
{{ myvar }}
You wanna hear a dirty joke?
{% include 'joke.txt' %}
""".strip())

# Writing the joke template
with open('joke.txt', 'w', encoding='utf-8') as file:
    file.write("""
A boy fell in a mud puddle. {{ myvar }} 
""".strip())

from jinja2 import Environment, FileSystemLoader

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader('.'))

# Render the base template with a variable
output = env.get_template('base.txt').render(myvar='Ha ha!')
print(output)
