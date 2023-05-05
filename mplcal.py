import datetime
from calendar import monthrange
from datetime import date, timedelta
import holidays


import matplotlib
import matplotlib.patches as patches
import matplotlib.pyplot as plt

import streamlit as st


def label_month(year, month, ax, i, j, cl="black"):
    months = [
        "Jan",
        "Fev",
        "Mar",
        "Abr",
        "Mai",
        "Jun",
        "Jul",
        "Ago",
        "Set",
        "Out",
        "Nov",
        "Dez",
    ]

    month_label = f"{months[month-1]} {year}"
    ax.text(i, j, month_label, color=cl, va="center")


def label_weekday(ax, i, j, cl="black"):
    x_offset_rate = 1
    for weekday in ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]:
        ax.text(i, j, weekday, ha="center", va="center", color=cl)
        i += x_offset_rate


def label_day(ax, day, i, j, cl="black"):

    ax.text(i, j, int(day), ha="center", va="center", color=cl)


def fill_box(ax, i, j):
    ax.add_patch(
        patches.Rectangle(
            (i - 0.5, j - 0.5),
            1,
            1,
            edgecolor="blue",
            facecolor="red",
            alpha=0.1,
            fill=True,
        )
    )

def check_color_day(year, month, day, weekday):
    if date(year, month, day) in holidays.Brazil()['{}-01-01'.format(year): '{}-12-31'.format(year)]:
        return "red"

    if weekday == 6:  # Sunday
        return "red"
    
    if weekday == 5:  # Saturday
        return "red"

    return "black"


def month_calendar(ax, year, month, fill):
    date = datetime.datetime(year, month, 1)

    weekday, num_days = monthrange(year, month)

    # adjust by 0.5 to set text at the ceter of grid square
    x_start = 1 - 0.5
    y_start = 5 + 0.5
    x_offset_rate = 1
    y_offset = -1

    label_month(year, month, ax, x_start, y_start + 2)
    label_weekday(ax, x_start, y_start + 1)

    j = y_start

    for day in range(1, num_days + 1):
        i = x_start + weekday * x_offset_rate
        color = check_color_day(year, month, day, weekday)

        if fill and check_fill_day(year, month, day, weekday):
            fill_box(ax, i, j)

        label_day(ax, day, i, j, color)
        weekday = (weekday + 1) % 7
        if weekday == 0:
            j += y_offset


def main(year, month, grid=False, fill=False):
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.axis([0, 7, 0, 7])
    ax.axis("off")

    if grid:
        ax.axis("on")
        ax.grid(grid)
        for tick in ax.xaxis.get_major_ticks():
            tick.tick1line.set_visible(False)
            tick.tick2line.set_visible(False)
            tick.label1.set_visible(False)
            tick.label2.set_visible(False)

        for tick in ax.yaxis.get_major_ticks():
            tick.tick1line.set_visible(False)
            tick.tick2line.set_visible(False)
            tick.label1.set_visible(False)
            tick.label2.set_visible(False)
    month_calendar(ax, year, month, fill)
    st.pyplot(fig=fig)

holiday_list = [
    (1, 1),
    (1, 10),
    (2, 11),
    (2, 23),
    (3, 21),
    (4, 29),
    (5, 3),
    (5, 4),
    (5, 5),
    (7, 18),
    (8, 11),
    (9, 19),
    (9, 23),
    (10, 10),
    (11, 3),
    (11, 23),
]
