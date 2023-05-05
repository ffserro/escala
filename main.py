import streamlit as st
import calendar
import holidays
from datetime import datetime as dt

ano = 2023

st.title('Escala de serviço')

meses = ['-', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
mes = meses.index(st.selectbox('Escolha o mês da escala a ser visualizada: ', meses))

st.write(mes)

feriados = holidays.Brazil()

st.write(feriados['2023-01-01': '2023-04-30'])

licpag = st.date_input('Qual é o dia da Licença Pagamento? ')
