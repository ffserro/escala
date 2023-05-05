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

licpag = st.date_input('Qual é o dia da Licença Pagamento? ',value=prm, min_value=prm, max_value=ult)

vermelha.append(licpag)
preta.remove(licpag)

vermelha.sort()

st.write(vermelha)
st.write(preta)

