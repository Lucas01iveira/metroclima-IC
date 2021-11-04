# Importando as bibliotecas relevantes
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import datetime as dt 

# Passos iniciais
df = pd.read_csv('CRDS_Jaragua_G2301_hour_LT.txt') # dataframe de trabalho
df = df.set_index('DATE_TIME') # definição da coluna 'DATE-TIME' como index
df.index = pd.to_datetime(df.index) # defino o index como um elemento data-hora

# -------------------------------------------------------------------------------------------------------
# Exercício 1
# Faça uma tabela com as médias mensais da variável de interesse para cada dia da semana.
# Para fins didáticos, considerarei a variável CO2_dry_m

# Crio uma nova coluna com os dias da semana
df['Weekday'] = df.index.dayofweek.map({
    0:'Mon',
    1:'Tue',
    2:'Wed',
    3:'Thu',
    4:'Fri',
    5:'Sat',
    6:'Sun'
})

# Obs.: o pandas já tem os comandos dayofweek, weekday e dayname imbutidos, mas estes só funcionam
# para elementos do tipo "DatetimeIndex". Como o index do nosso df já é um elemento desse tipo,
# basta utilizar os comandos tranquilamente.
# - Outra forma de criar essa coluna seria: df['weekdays'] = df.index.day_name() (sairiam os nomes em inglês)

q = df.groupby([df.index.strftime('%m-%b'), 'Weekday']).agg(['mean','std'])['CO2_dry_m'].unstack(level=0).round(2)

# Sugestão para colocar os dias da semana na ordem corrreta
df.groupby([df.index.strftime('%m-%b'), 'Weekday']).agg('mean')['CO2_dry_m'].unstack(level=0).round(2).loc[['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']]

# -------------------------------------------------------------------------------------------------------
# Exercício 2
# Faça uma tabela com as médias mensais da variável de interesse para cada hora do dia.

q = df.groupby([df.index.strftime('%m-%b'), df.index.hour]).agg('mean')['CO2_dry_m'].unstack(level=0).round(2)

# -------------------------------------------------------------------------------------------------------
# Exercício 3
# a) Encontre o mês com o menor valor médio da variável de interesse
# b) Crie uma tabela com a diferença entre o valor médio de cada mês e o valor médio do mês do item a
# c) Crie uma tabela similar ao item b, porém com o aumento percentual

# item a
a = df.groupby(df.index.month).agg('mean')['CO2_dry_m'].idxmin()

# item b
# defino uma função que calcula a diferença entre o valor médio do mês e o valor médio do mês que contém o menor ppm de CO2
def dif(series):
    return series.mean() - df[df.index.month == a].mean()['CO2_dry_m']

q = df.groupby(df.index.month).agg(['mean', dif])['CO2_dry_m']
# Funcionamento da função dif: as "series" que tão entrando lá são os conjuntos de dados da coluna df['CO2_dry_m'] 
# para cada mês. Então, para cada mês, o que a função dif ta fazendo é tirar uma diferença da média desse conjunto mensal inteiro e 
# subtraindo de um dado valor (no caso, a média do mês que conteve o menor ppm de co2)
print(q.head())

# item c
# defino uma função que calcula o aumento percentual
def percent_increase(series):
    return ((series.mean() - df[df.index.month == a].mean()['CO2_dry_m'])/df[df.index.month == a].mean()['CO2_dry_m'])*100

q = df.groupby(df.index.month).agg(['mean', dif, percent_increase])['CO2_dry_m']
print(q.head())

# -------------------------------------------------------------------------------------------------------
# Exercício 4
# Faça um gráfico do ciclo diurno para cada dia da semana na mesma figura

# Crio um novo dataframe com os médias diurnas para cada dia da semana
# df_day_hour = df.groupby(['Weekday',df.index.hour]).agg('mean')['CO2_dry_m']

plt.title('Diurnal cycle')
plt.ylabel('$CO_2$ [ppm]')
plt.xlabel('Day hour')
plt.grid()
sns.lineplot(
    data=df,
    x=df.index.hour,
    y=df['CO2_dry_m'],
    hue=df['Weekday'],
    hue_order=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    ci=0,
)
#plt.show()

# -------------------------------------------------------------------------------------------------------
# Exercício 5
# Faça um gráfico simlar ao do exercício anterior para as estações do ano (ao invés dos dias da semana)

# Removo o mês de dezembro do data frame:
df = df[df.index.month < 12]

# Crio uma nova coluna as estações do ano
aux = (df.index.month % 12 +3)//3
df['Season'] = aux.map({
    1:'Summer',
    2:'Autumn',
    3:'Winter',
    4:'Spring'
})

plt.title('Sazonal variation')
plt.xlabel('Day hour')
plt.ylabel('$CO_2$ [ppm]')
plt.grid()
sns.lineplot(
    data=df,
    x=df.index.hour,
    y=df['CO2_dry_m'],
    hue=df['Season'],
    hue_order=['Summer', 'Autumn', 'Winter', 'Spring'],
    ci=0
)
#plt.show()

# -------------------------------------------------------------------------------------------------------
# Exercício 6
# Crie um novo dataframe para a série completa com as médias diárias

ds = df['CO2_dry_m'].resample('d').mean().round(2)
