import pandas as pd
import matplotlib.pyplot as plt

# Lê o relatório que o DuckDB gerou
df = pd.read_csv('relatorio_mercado_ti.csv', sep=';')

# Filtra para pegar o Top 5 Cursos com mais alunos
top_cursos = df.groupby('Nome_Curso')['Total_Alunos'].sum().nlargest(5).index
df_top = df[df['Nome_Curso'].isin(top_cursos)]

# Cria uma tabela dinâmica para o gráfico (Cursos nas linhas, Tipo de Faculdade nas colunas)
pivot_df = df_top.pivot(index='Nome_Curso', columns='Tipo_Faculdade', values='Total_Alunos')

# Configura o gráfico
ax = pivot_df.plot(kind='barh', stacked=True, figsize=(10, 6), color=['#2ecc71', '#3498db'])

plt.title('Distribuição de Alunos em TI: Pública vs Privada (Censo 2023)')
plt.xlabel('Quantidade de Alunos')
plt.ylabel('Curso')
plt.tight_layout()

# Salva a imagem
plt.savefig('grafico_censo.png')
print("🖼️ Gráfico salvo como 'grafico_censo.png'. Agora é só subir pro GitHub!")