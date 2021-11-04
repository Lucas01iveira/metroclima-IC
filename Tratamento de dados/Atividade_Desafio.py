# importo as bibliotecas importantes

import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns

# Defino o data frame de trabalho
df = pd.read_csv('CRDS_Jaragua_G2301_hour_LT.txt')
df = df.set_index('DATE_TIME')
df.index = pd.to_datetime(df.index)
df['Weekday'] = df.index.day_name()

# Crio um novo dataframe com os ciclos diurnos por dia da semana
ds = df.groupby(['Weekday',df.index.hour]).agg('mean')['CO2_dry_m'].round(2).loc[[
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday'
]]

#print(ds)

# Crio um dataframe para cada dia da semana
ds_mon = ds['Monday']
ds_tue = ds['Tuesday']
ds_wed = ds['Wednesday']
ds_thu = ds['Thursday']
ds_fri = ds['Friday']
ds_sat = ds['Saturday']
ds_sun = ds['Sunday']

# concateno tudo num dataframe só e reseto o index
ds_week = pd.concat([
    ds_mon,
    ds_tue,
    ds_wed,
    ds_thu,
    ds_fri,
    ds_sat,
    ds_sun
])
ds_week = ds_week.reset_index(drop=True)

#print(ds_week)


# Exercício: Reproduzir os gráficos da figura 7 do artigo de Paris 
fig, ax = plt.subplots(figsize=(9,6))

plt.title('Diunal cycle along week')
plt.ylabel('$CO_2$ [ppm]')
ax = sns.lineplot(
    data=ds_week,
    x=ds_week.index,
    y=ds_week,
    #marker='.',
    color='green',
    ci=None # Para que os gráficos não apresentem aquela "linhazinha clara" essa é a sintaxe que temos que usar
)

ax.set_xticklabels(['Mon','Mon','Tue','Wed','Thu','Fri','Sat','Sun','Mon'])
plt.show()
