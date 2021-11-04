# Importo as bibliotecas 
import pandas as pd
import statistics as s 

# O que deve ser feito:
# 1) Tabela com as médias e desvios para cada mês.
# 2) Tabela com as médias e desvios para cada estação do ano.
# 3) Tabela com o mínimo, máximo, amplitude e variação do ciclo diurno anual e para cada estação do ano.

# -------------------------------------------------------------------------------------------------------------------------
# Ajeito os valores floats para saírem com 2 casas decimais apenas
pd.options.display.float_format = '{:,.2f}'.format

# Defino o dataframe de trabalho:
df = pd.read_csv('CRDS_Jaragua_G2301_hour_LT.txt')
df = df.set_index('DATE_TIME') # defino o index como sendo a coluna 'DATE_TIME'
df.index = pd.to_datetime(df.index) # defino os indexs como elementos do tipo data 
df['month'] = df.index.strftime('%m') # crio uma coluna para os meses
df['hour'] = df.index.strftime('%H') # crio uma coluna para os horários


# -------------------------------------------------------------------------------------------------------------------------
# 1) Tabela com as médias e desvios para cada mês.

# Defino uma variável auxiliar "q" que contém os agrupamentos do df que eu preciso
q = df.groupby('month').agg(['mean','std'])['CO2_dry_m'].transpose()

# Passo para um arquivo de texto previamente criado
#q.to_csv('Org_months.txt')

# -------------------------------------------------------------------------------------------------------------------------
# 2) Tabela com as médias e desvios para cada estação do ano.

# Crio um backup do dataframe:
df_all = df.copy()

# Crio, no dataframe, a coluna com as estações do ano
# (para isso usaremos aquela operação definida convenientemente)
aux = (df.index.month % 12 + 3) // 3
df['season'] = aux.map({
    1:'Summer',
    2:'Autumn',
    3:'Winter',
    4:'Spring'
})

# Lembrando que o mês de dezembro de 2020 se enquadra como verão de 2021
# portanto não podemos utilizá-lo na análise sazonal de 2020
df = df[(df.index < '2020-12-01')]

# Defino uma variável auxiliar "q" que contém os agrupamentos do df que eu preciso
q = df.groupby('season').agg(['mean','std'])['CO2_dry_m'].transpose()[['Summer','Autumn','Winter','Spring']]
#print(q)


# Passo para um arquivo de texto previamente criado
#q.to_csv('Org_seasons.txt')

# -------------------------------------------------------------------------------------------------------------------------
# 3) Tabela com o mínimo, máximo, amplitude e variação do ciclo diurno anual e para cada estação do ano.

# Obs.: a "variação" do ciclo é definida como a média dos desvios-padrão associados ao valor de max e de min

# Definição da função que retorna a amplitude
def amplitude(series):
    return series.max() - series.min()
# Na qual o termo "series" representa uma linha / coluna do dataframe

# Passos para a construção da tabela (dataframe) com o ciclo diurno anual:
# i) Defino um novo dataframe com a média e o desv-pad diurno (anual)
ds = df.groupby('hour').agg(['mean','std'])['CO2_dry_m']
#print(ds)

# ii) Cálculo do valor máx, min, e da amplitude do ciclo diurno (anual)
a = ds['mean'].agg(['min','max',amplitude]).rename('Year')
#print(a)

# iii) Cálculo da variação do ciclo diurno (anual)
var = s.mean([ ds['std'][ds['mean'].idxmax()] , ds['std'][ds['mean'].idxmin()]])
var = pd.Series(var, name='Year', index=['var'])
#print(var)

# iv) Agrupamento de todos os cálculos numa única tabela (i.e., dataframe)
ds_year = ds['mean'].agg(['min','max', amplitude]).rename('Year').append(var).to_frame()
print(ds_year)

# Passos para a construção da tabela (dataframe) com o ciclo sazonal
# i) Defino um novo dataframe com a média e o desv-pad diurno (sazonal)
ds = df.groupby(['season','hour']).agg(['mean','std'])['CO2_dry_m'].unstack(level=0) # Utilizamos o df por conta da questão do mês de dez
#print(ds.head())

# ii) Cálculo do valor máx, min, e da amplitude diurna (sazonal)
a = ds['mean'].agg(['min','max',amplitude])
#print(a)

# iii) Cálculo da variação do ciclo diurno (sazonal)
var = []
for season in df.season.unique():
  var.append(((ds['std'][season][ds['mean'][season].idxmax()] + \
               ds['std'][season][ds['mean'][season].idxmin()])/2).round(2))
var = pd.DataFrame.from_dict({'var':var}, orient='index', columns=df.season.unique())
#print(var)

# iv) Agrupamento de todos os cálculos em uma única tabela (dataframe)
ds_seasons = ds['mean'].agg(['min', 'max', amplitude]).append(var)[['Summer','Autumn','Winter','Spring']]
#print(ds_seasons)

# Procedimento para juntar os dois data frames criados:
ds_completo = pd.concat([ds_year,ds_seasons],axis=1)[['Year','Summer','Autumn','Winter','Spring']]
#print(ds_completo)

print(df['CO2_dry_m'].idxmin().month)
# -------------------------------------------------------------------------------------------------------------------------
