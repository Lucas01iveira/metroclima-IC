# Importo as bibliotecas necessárias
import pandas as pd

# definindo o formato de saída dos valores float
pd.options.display.float_format = '{:,.2f}'.format
# Com isso todos os dados tipo float do df (definido nos moldes da biblioteca pandas)
# serão mostrados com apenas duas casas decimais

# Definição do data_frame
df = pd.read_csv('CRDS_Jaragua_G2301_hour_LT.txt')
df = df.set_index('DATE_TIME') # Defino os elementos da coluna "date_time" como index
df.index = pd.to_datetime(df.index) # Transformo esses "index's" num elemento do tipo data-hora
df['hour'] = df.index.strftime('%H') # criação de uma nova coluna para a hora
df['month'] = df.index.strftime('%m') # criação de uma nova coluna para o mês 
#print(df.head())

# -------------------------------------------------------------------------------------------------------------------------

# Filtragem de dados
# Mesmos operadores: ==, >, <, >=, <=
# Exemplos:

# 1 - Dados do mês de janeiro
print(df[df.index.month == 1])

# 2 - Datas em que o CO2 dry ultrapassou 450 ppm
print(df[df.CO2_dry_m >= 450].index)
# Interpretação do cógigo: dentro do df, eu estou selecionando aqueles
# em que a concentração de co2 (dentro da coluna de concentrações) é maior ou igual a 450
# o ".index" no fim entra para indicar que, desses elementos selecionados, eu quero ver o index (data/hora)

# 2a - Quais foram os valores que ultrapassaram
print(df[df.CO2_dry_m >= 450]['CO2_dry_m'])
# Mesma ideia: acesso os elementos da coluna CO2_dry_m maiores ou iguais a 450
# e com o 2º colchete eu indico que quero verificar quem são esses elementos

# 2b - Quantas ultrapassagens aconteceram
print(df[df.CO2_dry_m >= 450]['CO2_dry_m'].count())

# 3 - Duas ou mais condições
# 3a - Período específico entre datas
print(df[(df.index >= '2020-01-15') & (df.index <= '2020-01-20')])
# Dados coletados entre 15 de jan e 20 de jan

# 3b - Período específico entre duas datas com horas
print(df[(df.index >= '2020-01-15 00') & (df.index <= '2020-01-15 12')])
# Ou seja, quero ver todos os dados entre a 00h do dia 15 e 12h desse mesmo dia

# 3c datas em que o CO2 estava entre 400 ppm e 450 ppm
print(df[(df.CO2_dry_m >= 400) & (df.CO2_dry_m <= 450)].index)

# -------------------------------------------------------------------------------------------------------------------------

# Função "describe"
print(df.describe())
# Ele vai nos dar uma descrição geral dos valores do data frame: média, desv_pad, minimo, 1Q, 2Q, 3Q, máximo

# Para ver a descrição de colunas específicas, basta inserir, dentro de "df"
# a lista das colunas de interesse
print(df[['CO2_dry_m','CO2_m']].describe())

# Seleção de "agregation functions"
print(df.describe().loc[['mean','std']])
# No caso isso aqui a gente usa para selecionar específicamente quais linhas do describe
# nós temos interesse em mostrar

# Para salvar as informações do describe:
df.describe().loc[['mean','std']].to_csv('teste.txt', float_format='%.2f')

# -------------------------------------------------------------------------------------------------------------------------

# Função "groupby"
df.groupby('hour').mean()
# com isso ele está agrupando as médias de todas as colunas para cada hora do dia (incluindo todos os dados do df) numa tabela

# outra forma de fazer:
a = df.groupby(df.index.hour).mean()
#print(a.tail())

# Para mostrar os resultados do groupby (todos os dados do df) para uma coluna específica:
df.groupby(df.index.hour).mean()['CH4_m']

# É possível também agrupar mais de uma variável
df.groupby(['month','hour'])['CO2_dry_m'].mean()
# Ou seja: agrupando por mês e hora, os dados do CO2_dry_m médios
# (cada termo que a gente insere na lista do groupby é uma nova coluna resultante)

# Outra forma de fazer:
df.groupby([df.index.month,df.index.hour]).mean()['CO2_dry_m']

# Para agrupar mais de um cálculo:
df.groupby('hour').agg(['mean','std'])['H2O_m'].tail()
