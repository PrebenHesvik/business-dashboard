"""Components and modules"""
import dash_bootstrap_components as dbc
from dash import html

# Import components
from components import (
    dropdown,
    element_options,
    extended_card,
    radio_check,
    list_item
)

from load_datasets import options

# functions
from functions import (
    accounts_dict,
)

# accounts dictionary
acct_dict = accounts_dict()

# components
acct_category_options = [*acct_dict.keys()]
acct_category_options.insert(0, 'Alle')

account_categories = []
for i in range(1, 5):
    options_ = acct_category_options if i == 1 else {"label": "", "value": ""}
    value = 'Alle' if i == 1 else '-'

    d_down = dropdown(
        id=f'account_cat_{i}',
        value=value,
        options=options_,
        class_name='dropdown__transparent')

    account_categories.append(d_down)

show_options = ['Spend', 'Antall Faktura', 'Antall Leverandører']
show = dropdown(
    id='account-show',
    value='Spend',
    options=show_options)

frequency = dropdown(
    id='account-frequency',
    value='Q',
    options=options['frequency'])

years = element_options(options=options['year'])
years_checkboxes = radio_check(
    type='check',
    options=years,
    value=options['year'],
    id='account-years',
    class_name='switch',
    label='Velg År',
    with_col=True,
    col_class_name='switch-group',
    col_width=6,
    col_width_xl=4)

factories = element_options(options['factory'])
factory_checkboxes = radio_check(
    type='check',
    options=factories,
    value=options['factory'],
    id='account-locations',
    class_name='switch',
    label='Velg Fabrikk',
    with_col=True,
    col_class_name='switch-group')

# modules
select_accounts_row = dbc.Row(
    children=[
        dbc.Col(acct_cat, id=f'col_account_cat_{i}', width={"size": 3})
        for i, acct_cat in enumerate(account_categories, start=1)
    ],
    id='select-accounts-row',
    className='select-accounts-row',
    justify='center')

input_items = [list_item('Vis', show), list_item('Frekvens', frequency)]
main_inputs = extended_card(input_items, width=12)

switches = dbc.Row([years_checkboxes, factory_checkboxes], justify='center')

# layout
layout = html.Div([
    main_inputs,
    switches,
    select_accounts_row,
    dbc.Row(id='account-main-chart')
])
