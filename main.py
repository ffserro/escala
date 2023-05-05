import streamlit as st
import calendar
import holidays
from datetime import datetime as dt


st.title('Escala de serviço')

meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
mes = meses.index(st.selectbox(meses))

st.write(mes)


st.write(calendar.month(2023, 5))

feriados = holidays.Brazil()

st.write(feriados['2023-01-01': '2023-12-31'])

data = st.date_input('Entre com uma data')

try:
    dts = st.date_input(label='Date Range: ',
                value=(dt(year=2022, month=5, day=20, hour=16, minute=30), 
                        dt(year=2022, month=5, day=30, hour=16, minute=30)),
                key='#date_range',
                help="The start and end date time")
    st.write('Start: ', dts[0], "End: ", dts[1])

except:
    pass