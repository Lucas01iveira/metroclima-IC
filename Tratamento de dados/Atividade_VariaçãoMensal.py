# Importo as bibliotecas importantes
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 

print('_'*150)
print()

# Defino o dataframe de trabalho
df = pd.read_csv('CRDS_Jaragua_G2301_hour_LT.txt')

# Transformando a coluna de data/hora em índice
df = df.set_index('DATE_TIME')
df.index = pd.to_datetime(df.index)

# Criando uma nova variável "mês"
df['month'] = df.index.strftime('%m') 
# funcionamento da função strftime: strftime('%m / %d / %Y , %H:%M:%S');
# ou seja: m = month; d = day; Y = year; H = hour; M = minute; S = second 

fig, ax = plt.subplots(figsize=(9,6)) # defino a figura e ajeito o seu tamanho
ax = sns.boxplot(
    data=df, x='month', y='CO2_dry_m',
    color='lightgrey'
) # acrescento o box plot nessa figura

ax = sns.lineplot(
    data=df, x='month', y='CO2_dry_m',
    color='black',
    marker='o',
    #ci='sd'
    ci=0
) # acrescento o lineplot nessa figura

# Configurações de título e legenda:
plt.title('Monthly distribution', fontsize=16, fontweight='bold')
plt.xlabel('2020')
plt.ylabel('$CO_{2} \, \, (ppm)$')

# Inserindo os nomes dos meses no eixo x
ax.set_xticklabels(['Jan', 'Fev', 'Mar', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'])
'''
- xtick faz referência aos ticks do eixo x, ou seja, cada valor que é plotado no eixo x, no nosso caso, cada mês
- label é o nome que aparece em cada tick (se você quisesse, por exemplo,
diminuir o tamanho do gráfico, para ficar melhor ajustado, você poderia reduzir os "ticks" e colocar labels a cada 2 meses por exemplo)
'''
plt.show()

print()
print('_'*150)