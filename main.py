import streamlit as st
import calendar
import holidays
from datetime import datetime, date
ano = 2023

st.title('Escala de serviço')

meses = ['-', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
mes = meses.index(st.selectbox('Escolha o mês da escala a ser visualizada: ', meses))

prm = date(ano, mes, 1)
ult = date(ano, mes, calendar.monthrange(ano,mes)[-1])

st.write(mes)

feriados = holidays.Brazil()

st.write(feriados['{}-01-01'.format(ano): '{}-12-31'.format(ano)])

licpag = st.date_input('Qual é o dia da Licença Pagamento? ', min_value=prm, max_value=ult)
