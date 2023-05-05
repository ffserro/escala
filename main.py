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

feriados = holidays.Brazil()['{}-01-01'.format(ano): '{}-12-31'.format(ano)]

def iterdates(date1, date2):
    one_day = timedelta(days = 1)
    current = date1
    while current < date2:
        yield current
        current += one_day

for d in iterdates(prm, ult):
    if d.weekday() in (5, 6):
        vermalha.append(d)

st.write(vermelha)

licpag = st.date_input('Qual é o dia da Licença Pagamento? ',value=prm, min_value=prm, max_value=ult)
