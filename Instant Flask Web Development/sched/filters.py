"""Custom filters for Jinja templating. Load with init_app function."""
from markupsafe import escape, Markup
from jinja2 import pass_context
from markupsafe import Markup, escape


def init_app(app):
    app.jinja_env.filters['nl2br'] = do_nl2br


def do_datetime(dt, format=None):
    """Jinja template filter to format a datetime object with date & time."""
    if dt is None:
        # By default, render an empty string.
        return ''
    if format is None:
        # No format is given in the template call. Use a default format.
        #
        # Format time in its own strftime call in order to:
        # 1. Left-strip leading 0 in hour display.
        # 2. Use 'am' and 'pm' (lower case) instead of 'AM' and 'PM'.
        formatted_date = dt.strftime('%Y-%m-%d - %A')
        formatted_time = dt.strftime('%I:%M%p').lstrip('0').lower()
        formatted = '%s at %s' % (formatted_date, formatted_time)
    else:
        formatted = dt.strftime(format)
    return formatted


def do_date(dt, format='%Y-%m-%d - %A'):
    """Jinja template filter to format a datetime object with date only."""
    if dt is None:
        return ''
    # Only difference with do_datetime is the default format, but that is
    # convenient enough to warrant its own template filter.
    return dt.strftime(format)


def do_duration(seconds):
    """Jinja template filter to format seconds to humanized duration.

    3600 becomes "1 hour".
    258732 becomes "2 days, 23 hours, 52 minutes, 12 seconds".
    """
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    tokens = []
    if d > 1:
        tokens.append('{d} days')
    elif d:
        tokens.append('{d} day')
    if h > 1:
        tokens.append('{h} hours')
    elif h:
        tokens.append('{h} hour')
    if m > 1:
        tokens.append('{m} minutes')
    elif m:
        tokens.append('{m} minute')
    if s > 1:
        tokens.append('{s} seconds')
    elif s:
        tokens.append('{s} second')
    template = ', '.join(tokens)
    return template.format(d=d, h=h, m=m, s=s)


@pass_context
def do_nl2br(ctx, value):
    """Convert newlines to <br> tags."""
    escaped_value = escape(value)
    return Markup(escaped_value.replace('\n', '<br>'))