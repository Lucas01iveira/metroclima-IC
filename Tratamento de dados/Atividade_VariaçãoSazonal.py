# importo as bibliotecas importantes 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# defino o data frame de trabalho
df = pd.read_csv('CRDS_Jaragua_G2301_hour_LT.txt')

# Configuro a coluna DATE_TIME como índice
df = df.set_index('DATE_TIME') # defino a coluna 'DATE_TIME' como index
df.index = pd.to_datetime(df.index) # coloco os índices como uma data (no próprio python)

# Criar uma nova coluna, dentro desse data frame, que represente as estações do ano
'''
Q ideia é associar números para uma dada estação de modo que, fazendo operações com
os meses do ano, o resultado seja o número da estação correspondente.

Operação boa:
(mês % 12 + 3)//3
'''

df['seasons']=((df.index.month % 12 + 3)//3).map({1:'Summer',2:'Autumn',3:'Winter',4:'Spring'})
# Lembrando que o mês de dezembro contaria como verão de 2021, então temos que excluí-lo do nosso data frame para fazer o plot
df = df[(df.index < '2020-12-01')] # atualizo o data frame com os dados de todos os índices menores que 2020-12-01 (início de dez)

# Configurações do boxplot
sns.boxplot(data=df, x='seasons', y='CO2_dry_m')
plt.title('Seasonal variation')
plt.ylabel('$CO_2 \, (ppm)$')
# Com os códigos anteriores o eixo x ja vem automaticamente corrigido
plt.show()

# Se quiséssemos plotar o box plot junto com uma curva
fig,ax = plt.subplots(figsize=(9,6))

ax = sns.boxplot(data=df, x='seasons', y='CO2_dry_m')
ax = sns.lineplot(data=df, x='seasons',y='CO2_dry_m', ci=0, color='black',marker='o')
plt.title('Seasonal variation',fontsize=15, fontweight='bold')
plt.ylabel('$CO_2 \, (ppm)$',fontsize=12) # Aqui o "fontsize" mexe no tamanho da letra da legenda do eixo y
plt.xlabel('Seasons of the year',fontsize=12) # Aqui o "fontsize" mexe no tamanho da letra da legenda do eixo x
plt.xticks(fontsize=10) # Aqui o "fontsize" mexe no tamanho dos números do eixo y (gráfico)
plt.yticks(fontsize=10) #  Aqui o "fontsize" mexe no tamanho dos números do eixo x (gráfico)
plt.grid(linestyle='-.')
plt.show()