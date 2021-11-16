import dash_bootstrap_components as dbc


def radio_check(
        type, options, value, id='', class_name='', label=None,
        form_text=None, switch=True, inline=True, with_col=True,
        col_id='', col_class_name='', col_width=6,
        col_width_xl=6):

    if label is not None:
        label = dbc.Label(label)

    if form_text is not None:
        form_text = dbc.FormText(form_text)

    if type == 'check':
        element = dbc.Checklist(
            options=options, value=value, id=id,
            className=class_name, switch=switch,
            inline=inline)
    else:
        element = dbc.RadioItems(
            options=options, value=value, id=id,
            className=class_name, switch=switch,
            inline=inline)

    form_group = [label, element, form_text]

    if with_col is not False:
        return dbc.Col(
            form_group, id=col_id, className=col_class_name,
            width=col_width, xl=col_width_xl)
    else:
        return form_group
