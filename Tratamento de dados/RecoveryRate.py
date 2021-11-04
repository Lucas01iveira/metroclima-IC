# Importando as bibliotecas importantes 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Definindo o data frame de trabalho
df = pd.read_csv('CRDS_Jaragua_G2301_hour_LT.txt')
df = df.set_index('DATE_TIME')
df.index = pd.to_datetime(df.index)

'''
Sempre é bom relembrar

- Para colocar uma tabela/dataframe (seja um dataframe construido
pelo groupby, por exemplo, ou seja lá qual dataframe for) os comandos que 
podem ser utilizados são:
.to_frame()
.unstack(level=0)

- Para mais exemplos de apresentação de resultados verificar os códigos
das atividades desenvolvidas
'''

# Agrupando pelas médias mensais:
a = df.groupby(df.index.month).agg('mean')['CO2_dry_m']
#print(a.to_frame())

# Mas como sabemos se essas médias são de fato representativas? Pode ser que alguns desses meses tenham uma quantidade
# significativa de dados faltando.

# Calculando a quantidade de dados válidos no dataframe

print(len(df['CO2_dry_m'])) # dá a quantidade total de linhas (independente se tem um dado ou não)
print(df['CO2_dry_m'].count()) # dá a quantidade de linhas com valores válidos

print(df['CO2_dry_m'].notnull().sum()) 
# para cada linha com valor não nulo (i.e., igual a "True" pela sintaxe colocada) o programa soma +1
# ao final é retornado o valor total somado

print(df['CO2_dry_m'].isnull().sum())
# para cada linha com valor nulo (i.e., igual a "True" pela sintaxe colocada) o programa soma +1
# ao final é retornado o valor total somado

# Contando a quantidade de dados válidos em cada mês:
a = df.groupby(df.index.month).agg('count')['CO2_dry_m'] 
print(a.to_frame())

# Incluindo uma coluna de disponibilidade no data frame :
df['avail'] = df['CO2_dry_m'].notnull()
print(df.head())

# Ao agrupar as médias da coluna avail, o programa irá retornar a porcentagem de valores "True" (média de contagens com 0 e 1),
# i.e, o número de dados não nulos dividido pelo número de dados totais

a = df.groupby(df.index.month).mean()[['CO2_dry_m','avail']]
print(a)

# Note que o mês de outubro, por exemplo, é o pior de todos (66.9% de valores válidos)

'''
O ponto é: o cálculo feito anteriormente representa sim um recovery rate, mas um recovery rate de um dataframe
incompleto. Ou seja, estamos calculando o recovery rate dos valores disponíveis, mas não dos meses inteiros.
Exemplo: para o mês de dezembro os dados só vão até as 18h do dia 13 (então o valor calculado para o mês de dezembro não 
é representativo para o mês em si).

Obs.: isso não impacta nos valores de média/variação que utilizamos para análise (porque essas contas de fato não considerariam 
os valores nulos que serão incluidos quando o data frame for "preenchido"; são dados ausentes mesmo), mas 
para calcular a taxa de recuperação é necessário corrigir isso
'''

# Então, o primeiro passo para obter as taxas de recuperação corretas é preencher o dataframe

r = pd.date_range(start='2020-01-01 00', end='2020-12-31 23', freq='H')
# criação de um range de datas completo desde a 00h de 01/jan até 23h de 31/dez

ds = df.reindex(r)  # readequação dos índices para o range de datas criado
# Com isso o dataframe ds passa agora a ter, onde nem havia dados, valores NaN 
# (os quais contabilizam para o .isnull())

print(len(ds['CO2_dry_m']))

# Faço os mesmos procedimentos anteriores, mas agora para o dataframe ds (= df completo)
ds['avail'] = ds['CO2_dry_m'].notnull()
a = ds.groupby(ds.index.month).mean()[['CO2_dry_m','avail']]
print(a)

# Agora sabemos que os valores das taxas de recuperação obtidos são representativos de cada mês.
# Perceba que dezembro, na verdade, é o "pior" de todos