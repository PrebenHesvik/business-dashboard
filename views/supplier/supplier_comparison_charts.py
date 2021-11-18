from .account_chart import account_chart

# identify top 5 account_descriptions associated with
# the supplier, and chart top 10 suppliers in each
# account descriptions in terms of spend and number
# of invoices. Add supplier to chart if supplier is
# not among top ten

def supplier_comparison_charts(df, accounts, supplier, chart_size, ChartData):
    chart_data_list = []

    for account in accounts:
        # supplier spend for account
        data, title, marker_colors = account_chart(
            df, account, supplier)

        account_spend = ChartData(
            data=data, title=title,
            chart_type='bar', marker_colors=marker_colors,
            orientation='h', width=chart_size[0])

        chart_data_list.append(account_spend)

        # supplier invoices for account
        data, title, marker_colors = account_chart(
            df, account, supplier,
            keyword='Antall Faktura')

        account_invoices = ChartData(
            data=data, title=title,
            chart_type='bar', marker_colors=marker_colors,
            orientation='h', width=chart_size[0])

        chart_data_list.append(account_invoices)
    return chart_data_list