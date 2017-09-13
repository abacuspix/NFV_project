from flask.ext.restless import ProcessingException
from app import api
from entries.forms import CommentForm
from models import Comment


def post_preprocessor(data, **kwargs):
    form = CommentForm(data=data)
    if form.validate():
        return form.data
    else:
        raise ProcessingException(
            description='Invalid form submission.', code=400)


api.create_api(
    Comment,
    methods=['GET', 'POST'],
    include_columns=['id', 'name', 'url', 'body',
                     'created_timestamp'],
    include_methods=['gravatar'],
    preprocessors={
        'POST': [post_preprocessor],
    })
