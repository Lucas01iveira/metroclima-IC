# Importando bibliotecas importantes 
import pandas as pd # tratamento de tabelas
import matplotlib.pyplot as plt # tratamento de gráficos 
import seaborn as sns # tratamento de gráficos (+ funcionalidades extras)

print('_'*140)
print()

# Definição do data frame (tabela de dados)
df = pd.read_csv('CRDS_Jaragua_G2301_hour_LT.txt')
# print(df.head()) # apresento as 5 primeiras linhas da tabela

print()

# Transformando a coluna de data/hora em índice
df = df.set_index('DATE_TIME')
df.index = pd.to_datetime(df.index) # Transforma os índices setados na linha anterior em um objeto "data-hora" para manipulação
# print(df.head())

# Plotando os dados com o pandas
df.CO2_dry_m.plot()
plt.show()

# Plotando com o matplotlib
plt.plot(df.CO2_dry_m)
plt.show()

# Plotando com o seaborn
sns.lineplot(data=df, x=df.index, y='CO2_dry_m')
plt.show()

# Criando uma variável "hora"
df['hour'] = df.index.strftime('%H')


# Gráfico de box plot da variação diurna (i.e., ao longo de um dia)
sns.boxplot(data=df, x='hour', y='CO2_dry_m')
plt.show()

# Gráfico de linha da variação diurna 
sns.lineplot(data=df, x='hour', y='CO2_dry_m')
plt.show()

# Alterando características do gráfico
# Defino a figura 'ax'
fig, ax = plt.subplots(figsize=(9,6)) # tamanho da figura

# Acrescento o boxplot nessa figura
ax = sns.boxplot(
data=df, x='hour', y='CO2_dry_m', # settando os parâmetros do gráfico
color='lightgrey', # mesma cor para todos os elementos,
showfliers=False, # não mostra os outliers (pontos mais externos do boxplot)
)

# Acrescento o lineplot nessa figura
ax = sns.lineplot(
data=df, x='hour', y='CO2_dry_m',
color='black',
marker='o',
#ci='sd'
ci = 0 # isso aqui é pra não mostrar nenhum sombreado em torno da linha do gráfico
)
# By the way, o sombreado representa o "intervalo de confiança" dos dados

# Definindo título do gráfico e dos eixos
plt.title('Diurnal variation', fontsize= 16, fontweight='bold')
plt.xlabel('Hour (local time)',fontsize='16')
plt.ylabel('$CO_2 \; (ppm)$', fontsize= 16)

# Tamanho dos valores dos eixos
ax.tick_params(axis='x', labelsize=14)
ax.tick_params(axis='y', labelsize=14)

# Grid do gráfico (o que é isso?)
plt.grid(axis='both', which='major', linestyle='--')

plt.show()

print()
print('_'*140)

