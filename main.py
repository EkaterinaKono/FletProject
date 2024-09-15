import flet as ft
import datetime
import csv
from csv import writer
import matplotlib
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart
import pandas as pd
from model import ExpData

matplotlib.use("svg")


def main(page: ft.Page):

    a = None
    existing_rows = []

    def date_determination(e):
        calendar.text = f"{e.control.value.strftime('%d-%m-%Y')}"
        calendar.update()

    page.title = "Органайзер расходов"
    page.window.width = 800
    page.window.height = 1000

    expenses_text = ft.Text('Выберите категорию расходов')
    expenses_dropdown = ft.Dropdown(width=300,
                                    options=[
                                        ft.dropdown.Option('Жилье'),
                                        ft.dropdown.Option('Еда'),
                                        ft.dropdown.Option('Одежда'),
                                        ft.dropdown.Option('Авто'),
                                        ft.dropdown.Option('Медицина'),
                                        ft.dropdown.Option('Страхование'),
                                        ft.dropdown.Option('Образование'),
                                        ft.dropdown.Option('Личные расходы'),
                                        ft.dropdown.Option('Электроника'),
                                        ft.dropdown.Option('Товары для детей'),
                                        ft.dropdown.Option('Зоотовары'),
                                        ft.dropdown.Option('Подарки'),
                                        ft.dropdown.Option('Отдых и развлечения'),
                                        ft.dropdown.Option('Налоги')]
                                    )

    date = ft.DatePicker(
        first_date=datetime.datetime(year=2023, month=1, day=1),
        last_date=datetime.datetime(year=2025, month=12, day=31),
        on_change=date_determination
        )

    calendar = ft.ElevatedButton(text='Укажите, когда были произведены расходы',
                                 icon=ft.icons.CALENDAR_MONTH,
                                 on_click=lambda e: page.open(date))

    expenses_count = ft.TextField(label='Сколько было потрачено', width=300)

    with open('expenses_file.csv', mode='w', encoding="utf8") as csvfile:
        file_writer = csv.writer(csvfile)
        file_writer.writerow(['date', 'category', 'amount'])

    def add_button_clicked(e):
        nonlocal existing_rows
        nonlocal expenses_count
        nonlocal a

        try:
            exp_data = ExpData(
                exp_date=date.value,
                exp_category=expenses_dropdown.value,
                exp_amount=expenses_count.value
                )

            new_row = [ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(date.value.strftime('%d-%m-%Y'))),
                    ft.DataCell(ft.Text(expenses_dropdown.value)),
                    ft.DataCell(ft.Text(expenses_count.value))
                ])
            ]

            existing_rows += new_row

            exp_date = date.value.strftime('%d-%m-%Y')
            exp_category = expenses_dropdown.value
            exp_amnt = expenses_count.value
            new_fields = [exp_date, exp_category, exp_amnt]

            with open('expenses_file.csv', mode='a', encoding="utf8") as f_object:
                writer_object = writer(f_object, lineterminator='\r')
                writer_object.writerow(new_fields)

            expenses_table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Дата")),
                    ft.DataColumn(ft.Text("На что потрачено")),
                    ft.DataColumn(ft.Text("Сумма, руб"), numeric=True)
                ],
            )

            expenses_table.rows = existing_rows

            page.clean()

            my_lv.controls.append(expenses_table)

            calendar.text = 'Укажите, когда были произведены расходы'
            expenses_dropdown.value = ''
            expenses_count.value = ''
            page.add(my_lv)
            my_lv.controls.remove(expenses_table)
            a = expenses_table
            return a

        except Exception as ex:
            page.add(ft.Text(f"Error: {ex}", color=ft.colors.RED))

    def pie_button_clicked(e):
        nonlocal a

        expenses = pd.read_csv('expenses_file.csv')

        fig, ax = plt.subplots()

        subexpenses = expenses.groupby(['category']).sum()
        subexpenses.to_csv('subexpenses_file.csv')
        subexp = pd.read_csv('subexpenses_file.csv')

        ax.pie(subexp['amount'], labels=subexp['category'], autopct='%1.0f%%')
        ax.set_title(f"Расходы, {subexp['amount'].sum()} руб.")
        fig.set_figwidth(7)
        chart = MatplotlibChart(fig, expand=False)

        my_lv.controls.append(a)
        my_lv.controls.append(chart)
        page.update()

        my_lv.controls.remove(a)
        my_lv.controls.remove(chart)

    add_button = ft.ElevatedButton('Добавить в таблицу', on_click=add_button_clicked)
    pie_button = ft.ElevatedButton('Посмотреть расходы на диаграмме', on_click=pie_button_clicked)

    my_lv = ft.ListView(expand=1, spacing=10, padding=10, auto_scroll=False, width=780)

    my_lv.controls.append(expenses_text)
    my_lv.controls.append(expenses_dropdown)
    my_lv.controls.append(calendar)
    my_lv.controls.append(expenses_count)
    my_lv.controls.append(add_button)
    my_lv.controls.append(pie_button)
    page.add(my_lv)


ft.app(target=main)
