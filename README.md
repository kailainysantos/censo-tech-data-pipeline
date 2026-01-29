# 📊 Censo Tech Analytics: Pipeline de Dados Educacionais

![Badge Status](http://img.shields.io/static/v1?label=STATUS\&message=CONCLUIDO\&color=GREEN\&style=for-the-badge)
![Badge Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge\&logo=python)
![Badge DuckDB](https://img.shields.io/badge/Engine-DuckDB-yellow?style=for-the-badge\&logo=duckdb)
![Badge ETL](https://img.shields.io/badge/Pipeline-ETL-orange?style=for-the-badge)

> **Projeto de Engenharia de Dados** desenvolvido para processamento e análise de microdados públicos do INEP (Censo da Educação Superior 2023), focado em resolver problemas de Big Data Local e otimização de memória.

---

## 📑 Índice

* [Sobre o Projeto](#sobre)
* [O Desafio Técnico](#desafio)
* [Arquitetura da Solução](#arquitetura)
* [Tecnologias Utilizadas](#tech)
* [Roadmap do Projeto](#roadmap)
* [Resultados e Visualização](#resultados)
* [Como Executar](#executar)
* [Autor](#autor)

---

## <a id="sobre"></a>🧐 Sobre o Projeto

O **Censo Tech Analytics** é uma solução de *Data Engineering* criada para mapear o cenário da educação superior em Tecnologia no Brasil. O projeto ingere dados reais e brutos do governo para responder questões de negócio sobre a oferta de cursos (Engenharia de Dados, Ciência da Computação, SI) e a predominância do ensino privado versus público.

Os dados utilizados são oficiais, provenientes do [Portal de Dados Abertos do INEP](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-da-educacao-superior).

---

## <a id="desafio"></a>⚡ O Desafio Técnico

Os arquivos de microdados do Censo (dataset `MICRODADOS_CADASTRO_CURSOS`) possuem estrutura complexa e alta volumetria.
A abordagem tradicional de carregar todo o dataset em memória (ex: Pandas puro `read_csv`) em hardware convencional (Notebook i5, 12GB RAM) é inviável para processamento ágil, frequentemente causando travamentos.

**A Solução:** Implementação de um pipeline **ELT** baseado no **DuckDB**, um motor SQL OLAP embutido que permite:

1. **Processamento Out-of-Core:** Manipulação de dados maiores que a RAM disponível.
2. **Streaming de Dados:** Leitura otimizada do CSV bruto sem carga total.
3. **Alta Performance:** Execução de queries analíticas vetorizadas em segundos.

---

## <a id="arquitetura"></a>🛠 Arquitetura da Solução

O pipeline segue o padrão **ETL (Extract, Transform, Load)**:

1. **Extract (Ingestão):** Conexão direta com o arquivo CSV bruto via DuckDB.
2. **Transform (Processamento):**

   * Filtragem de cursos alvo via `SQL` (`ILIKE`).
   * Normalização de dados categóricos (De-para: Pública/Privada).
   * Agregação de métricas (Soma de matrículas, Contagem de ofertas).
3. **Load & Viz (Entrega):**

   * Exportação dos dados refinados para `.csv`.
   * Geração automática de visualização gráfica estática com `Matplotlib`.

### Query Principal (DuckDB)

```sql
SELECT 
    NO_CINE_ROTULO as Nome_Curso,
    CASE WHEN TP_REDE = 1 THEN 'Pública' ELSE 'Privada' END as Tipo_Faculdade,
    SUM(QT_MAT) as Total_Alunos
FROM read_csv('dados/MICRODADOS_CADASTRO_CURSOS_2023.CSV', auto_detect=True, encoding='latin-1')
WHERE NO_CINE_ROTULO ILIKE '%Engenharia de Dados%'
GROUP BY Nome_Curso, Tipo_Faculdade
ORDER BY Total_Alunos DESC
```

## <a id="tech"></a>🧰 Tecnologias Utilizadas

As ferramentas foram escolhidas com foco em **performance**, **simplicidade** e **reprodutibilidade** do pipeline:

* **Linguagem:** Python 3.12
* **Engine de Processamento:** DuckDB (OLAP Database)
* **Análise de Dados:** Pandas (refinamento final dos dados)
* **Visualização:** Matplotlib (geração de gráficos estáticos)
* **Controle de Versão:** Git & GitHub

---

## <a id="roadmap"></a>🗺 Roadmap do Projeto

As etapas de desenvolvimento foram organizadas e rastreadas via **GitHub Projects**, seguindo uma evolução incremental do pipeline:

* [x] **Configuração de Ambiente:** Setup do Python, Virtualenv e DuckDB.
* [x] **Engenharia de Dados (ETL):** Script de ingestão e limpeza dos microdados do INEP.
* [x] **Análise Exploratória:** Query SQL para categorização do ensino Público vs Privado.
* [x] **Visualização de Dados:** Script Python para geração automática de gráficos.
* [ ] **Expansão:** Análise por Região Geográfica (Norte, Sul, Nordeste).

---

## <a id="resultados"></a>📊 Resultados e Visualização

O pipeline gerou com sucesso uma análise do mercado educacional de cursos de Tecnologia no Brasil. O gráfico final é produzido automaticamente a partir dos dados processados pelo DuckDB e refinados em Python.

**Análise:** Os resultados indicam uma **predominância massiva do setor privado** na oferta de vagas para cursos de tecnologia, reforçando a relevância de políticas públicas, programas de bolsa e financiamento estudantil para ampliar o acesso a essas carreiras.

![Distribuição do Mercado de TI](grafico_censo.png)

---

## <a id="executar"></a>💻 Como Executar

### Pré-requisitos

* Python 3.8+
* Git

### Passo a passo

1. **Clone o repositório:**

```bash
git clone https://github.com/kailainysantos/censo-tech-data-pipeline.git
cd censo-tech-data-pipeline
```

2. **Obtenha os dados:**

   * Baixe o *Censo da Educação Superior 2023* no site do INEP.
   * Extraia o arquivo `MICRODADOS_CADASTRO_CURSOS_2023.CSV`.
   * Coloque o arquivo na pasta `dados/` dentro do projeto.

3. **Instale as dependências:**

```bash
pip install duckdb pandas matplotlib
```

4. **Execute o pipeline:**

```bash
# 1. Processar os dados (gera o CSV limpo)
python analise_cursos.py

# 2. Gerar o gráfico (gera a imagem PNG)
python gerar_grafico.py
```

---

## <a id="autor"></a>👩‍💻 Autor

Desenvolvido por **Kailainy Santos Souza**, com foco em **Engenharia de Dados** e **Big Data Analytics**, utilizando dados públicos reais para resolução de problemas analíticos em ambiente local.
