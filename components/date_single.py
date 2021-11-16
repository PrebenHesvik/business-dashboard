from dash import dcc
import datetime as dt
from dateutil.parser import parse


def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


def date_single(id, min_date=None, max_date=None, init_date=None,
                df=None, date_col=None, classes=None):
    if min_date is None:
        min_date = df[date_col].min().to_pydatetime()

    if max_date is None:
        max_date = df[date_col].max().to_pydatetime()

    classes = 'datepicker ' + classes if classes is not None else 'datepicker'

    if isinstance(init_date, dt.date):
        date = init_date
    elif init_date == 'start':
        date = min_date
    elif init_date == 'end':
        date = max_date
    elif init_date == 'today':
        date = dt.datetime.today().strftime('%Y-%m-%d')

    return dcc.DatePickerSingle(
        id=id,
        className=classes,
        min_date_allowed=min_date,
        max_date_allowed=max_date,
        initial_visible_month=date,
        date=date,
        with_portal=False,
        display_format='MMMM Y, DD',
    )
