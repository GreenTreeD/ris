from flask import render_template, session


def render_with_defaults(template_name, **kwargs):
    default_context = {
        'user_role': session.get('user_role', 'unauth')
    }
    context = {**default_context, **kwargs}
    return render_template(template_name, **context)