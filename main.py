import streamlit as st
import calendar
import holidays
from datetime import datetime, date, timedelta
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

from calendar_view.calendar import Calendar
from calendar_view.core import data
from calendar_view.core.event import Event

config = data.CalendarConfig(
    lang='pt-br',
    title='Escala de Serviço - {}'.format(meses[mes]),
    dates='{} - {}'.format(prm, ult),
    show_year=True,
    mode='working_hours',
    legend=False,
)
events = [
    Event('Planning', day='2019-09-23', start='11:00', end='13:00'),
    Event('Demo', day='2019-09-27', start='15:00', end='16:00'),
    Event('Retrospective', day='2019-09-27', start='17:00', end='18:00'),
]

data.validate_config(config)
data.validate_events(events, config)

calendar = Calendar.build(config)
calendar.add_events(events)
calendar.save("sprint_23.png")
st.image("sprint_23.png")