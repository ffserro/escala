import streamlit as st
import calendar
import holidays
from datetime import datetime, date, timedelta
import matplotlib.pyplot as plt

ano = 2023

st.title('Escala de serviço')

meses = ['-', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
mes = meses.index(st.selectbox('Escolha o mês da escala a ser visualizada: ', meses))

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

licpag = st.date_input('Qual é o dia da Licença Pagamento? ',value=min(preta), min_value=prm, max_value=ult)

vermelha.append(licpag)
preta.remove(licpag)

vermelha.sort()

from mplcal import main

global fillday_list
global holiday_list

fillday_list = [(12, 24), (12, 25)]

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

main(ano, mes, grid=False, fill=False)