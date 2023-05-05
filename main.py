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

from mplcal import MplCalendar
feb = MplCalendar(2023, 2) # 2017, February
feb.add_event(1, '1st day of February')
feb.add_event(5, '         1         2         3         4         5         6')
feb.add_event(5, '123456789012345678901234567890123456789012345678901234567890')
feb.add_event(18, 'OSLL Field Maintenance Day')
feb.add_event(18, 'OSLL Umpire Mechanics Clinic')
feb.add_event(20, 'Presidents day')
feb.add_event(25, 'OSLL Opening Day')
feb.add_event(28, 'T-Ball Angels vs Dirtbags at OSLL')
feb.show()