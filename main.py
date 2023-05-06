import streamlit as st
import calendar
import holidays
from datetime import datetime, date, timedelta

from calendar import monthrange

import matplotlib
import matplotlib.patches as patches
import matplotlib.pyplot as plt

import pandas as pd 
import numpy as np

from openpyxl import Workbook, load_workbook
from tempfile import NamedTemporaryFile
from io import BytesIO

ano = 2023

# Título e Prompts
st.title('Escala de serviço')

meses = ['-', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
mes = meses.index(st.selectbox('Escolha o mês da escala a ser visualizada: ', meses))

if mes != 0:

    # Definições de data
    prm = date(ano, mes, 1)
    ult = date(ano, mes, calendar.monthrange(ano,mes)[-1])

    vermelha = []
    preta = []

    feriados = holidays.Brazil()['{}-01-01'.format(ano): '{}-12-31'.format(ano)]

    for single_date in (prm + timedelta(n) for n in range(calendar.monthrange(ano,mes)[-1])):
        if single_date.weekday() in (5,6):
            vermelha.append(single_date)

    for i in feriados:
        if i >= prm and i <= ult:
            vermelha.append(i)

    for single_date in (prm + timedelta(n) for n in range(calendar.monthrange(ano,mes)[-1])):
        if single_date not in vermelha:
            preta.append(single_date)

    licpag = st.date_input('Qual é o dia da Licença Pagamento? ',value=min(preta), min_value=prm, max_value=ult, key='licpag')

    vermelha.append(licpag)
    preta.remove(licpag)

    vermelha.sort()

    # Calendário
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
        if date(year, month, day) in vermelha:
            return "red"
        return "black"


    def month_calendar(ax, year, month, fill):
        date = datetime(year, month, 1)

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

            if fill and color == "red":
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

    main(ano, mes, grid=True, fill=True)

    # Divisão de serviço
    div_serv = {1:'CT Cespes',
                2:'CT Cassias',
                3:'CT Garcez',
                4:'CT Diogo',
                5:'CT Giovanni',
                6:'CT(QC-CA) Damasceno',
                7:'1T(IM) Sêrro',
                8:'SO-AM Anderson Santos',
                9:'SO-EL Alfredo',
                10:'SO-MO Alvarez'}

    workbook = load_workbook(filename='modelo.xlsx')
    tabela = workbook.active

    for i in range(calendar.monthrange(ano, mes)[-1]):
        tabela['A{}'.format(3+i)] = date(ano, mes, i+1).strftime('%d/%m/%y')
    
    for i in range(calendar.monthrange(ano, mes)[-1]):
        tabela['B{}'.format(3+i)] = ['SEG', 'TER', 'QUA', 'QUI', 'SEX', 'SAB', 'DOM'][date(ano, mes, i+1).weekday()]

    for i in range(calendar.monthrange(ano, mes)[-1]):
        tabela['C{}'.format(3+i)] = ['P', 'V'][date(ano, mes, 1+i) in vermelha]

    for i in range(len(div_serv)):
        tabela['I{}'.format(3+i)] = div_serv[1+i]

    if 'indisponivel' not in st.session_state:
        st.session_state.indisponivel = {}
    with st.form('indisponibilidade'):
        st.title('Adicionar indisponibilidades')
        mil_ind = st.selectbox('Selecione o militar com indisponibilidades:', list(div_serv.values()))
        per_ind = st.date_input('Qual é o período?', [])
        send_ind = st.form_submit_button('Enviar')
        if send_ind:
            st.session_state.indisponivel[mil_ind] = [per_ind[0] + timedelta(n) for n in range((per_ind[-1] - per_ind[0]).days)]
    st.write('Indisponíveis:')
    for i in st.session_state.indisponivel:
        st.write('{} indisponível entre {} e {}.'.format(i, st.session_state.indisponivel[i][0].strftime('%d/%m'), st.session_state.indisponivel[i][-1].strftime('%d/%m')))

    with st.form('inicio_tabela'):
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                p_1 = st.selectbox('Primeiro militar da escala preta', div_serv.values())
            with col2:
                v_1 = st.selectbox('Primeiro militar da escala vermelha', reversed(div_serv.values()))
            submit = st.form_submit_button('Gerar tabela')
    if submit:
        st.session_state.generated = True
    
    if st.session_state.generated:
        corrida = []

        nm_ver = list(reversed(div_serv.values()))[list(reversed(div_serv.values())).index(v_1):] + list(reversed(div_serv.values()))[:list(reversed(div_serv.values())).index(v_1)]
        nm_pre = list(div_serv.values())[list(div_serv.values()).index(p_1):] + list(div_serv.values())[:list(div_serv.values()).index(p_1)]

        for i in range(calendar.monthrange(ano, mes)[-1]):
            if date(ano, mes, i+1) in vermelha:
                corrida.append(nm_ver[0])
                nm_ver = nm_ver[1:] + [nm_ver[0]]
            if date(ano, mes, i+1) in preta:
                corrida.append(nm_pre[0])
                nm_pre = nm_pre[1:] + [nm_pre[0]]
        if 'df' not in st.session_state:
            st.session_state.df = pd.DataFrame({'Data':[date(ano, mes, i+1).strftime('%d/%m/%y') for i in range(calendar.monthrange(ano, mes)[-1])], 'Dia':[['SEG', 'TER', 'QUA', 'QUI', 'SEX', 'SAB', 'DOM'][date(ano, mes, i+1).weekday()] for i in range(calendar.monthrange(ano, mes)[-1])], 'Tab': [['P', 'V'][date(ano, mes, 1+i) in vermelha] for i in range(calendar.monthrange(ano, mes)[-1])], 'Nome': corrida})

        st.title('Trocas:')
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                de = st.date_input('De: ')
            with col2:
                para = st.date_input('Para: ')
            motivo = st.text_input('Motivo da troca')
            troca = st.button('Troca')
        if 'motivos' not in st.session_state:
            st.session_state.motivos = []
        if troca:
            idxa = st.session_state.df.Data.to_list().index(de.strftime('%d/%m/%y'))
            idxb = st.session_state.df.Data.to_list().index(para.strftime('%d/%m/%y'))
            nms = st.session_state.df.Nome.to_list()
            nms[idxa], nms[idxb] = nms[idxb], nms[idxa]
            st.session_state.df['Nome'] = nms        
            st.session_state.motivos.append('Troca entre os dias {} e {}. Motivo: {}'.format(de.strftime('%d/%m/%y'), para.strftime('%d/%m/%y'), motivo))
        
        st.dataframe(st.session_state.df.sort_values(by='Data'))

        st.table(st.session_state.motivos)

        for i in range(calendar.monthrange(ano, mes)[-1]):
            tabela['D{}'.format(3+i)] = st.session_state.df.Nome[i]
        
        for i in range(len(st.session_state.motivos)):
            tabela['F{}'.format(33+i)] = st.session_state.motivos[i]

        with NamedTemporaryFile() as tmp:
            workbook.save(tmp.name)
            data = BytesIO(tmp.read())

        st.download_button('Baixar tabela', data=data, mime='xlsx', file_name='tabela.xlsx')
