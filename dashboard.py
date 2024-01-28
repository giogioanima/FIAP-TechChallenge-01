import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import plotly.express as px
import plotly.figure_factory as ff



dados = pd.read_csv(r'ExpVinho 2022.csv', encoding='UTF-8', engine='python', sep=';', thousands='.', decimal=',')
pd.options.display.float_format = '{:.2f}'.format

dados = dados.drop('Id', axis=1)

dados.rename(columns={'País': 'pais'}, inplace = True)
dados = dados.set_index('pais')

dados_quantidade = dados
dados_quantidade = dados_quantidade.iloc[:, ::2]

dados_valor = dados
dados_valor = dados_valor.iloc[:, 1::2]

anual_qntd = dados_quantidade.T

anual_qntd_aberto = anual_qntd.reset_index().melt(id_vars=["index"], value_vars=anual_qntd.columns)
anual_qntd_aberto.columns = ["ano", "pais", "quantidade"]

anual_valor = dados_valor.T
anual_valor.index = anual_valor.index.str[0:4].str.strip()

anual_valor_aberto = anual_valor.reset_index().melt(id_vars=["index"], value_vars=anual_valor.columns)
anual_valor_aberto.columns = ["ano", "pais", "valor"]

from datetime import date

anual_qntd_aberto["ano"].astype("datetime64[ns]")
anual_valor_aberto["ano"].astype("datetime64[ns]")

anual_qntd_aberto["ano"] = pd.to_datetime(anual_qntd_aberto["ano"])
anual_qntd_aberto["ano"] = anual_qntd_aberto["ano"].dt.year
anual_qntd_aberto.info()

anual_valor_aberto["ano"] = pd.to_datetime(anual_valor_aberto["ano"])
anual_valor_aberto["ano"] = anual_valor_aberto["ano"].dt.year
anual_valor_aberto.info()

df_total = anual_qntd_aberto.join(anual_valor_aberto["valor"])

df_total["pais_origem"] = "Brasil"

df_total["pais"].unique()

continentes_dic = {
      "Afeganistão": "Ásia",
      "África do Sul": "África",
      "Alemanha, República Democrática": "Europa",
      "Angola": "África",
      "Anguilla": "América do Norte",
      "Antígua e Barbuda": "América Central",
      "Antilhas Holandesas": "América Central",
      "Argentina": "América do Sul",
      "Aruba": "América Central",
      "Austrália": "Oceania",
      "Áustria": "Europa",
      "Bahamas": "América do Norte",
      "Bangladesh": "Ásia",
      "Barbados": "América Central",
      "Barein": "Ásia",
      "Bélgica": "Europa",
      "Belice": "América Central",
      "Benin": "África",
      "Bolívia": "América do Sul",
      "Bósnia-Herzegovina": "Europa",
      "Brasil": "América do Sul",
      "Bulgária": "Europa",
      "Cabo Verde": "África",
      "Camarões": "África",
      "Canadá": "América do Norte",
      "Catar": "Ásia",
      "Cayman, Ilhas": "América do Norte",
      "Chile": "América do Sul",
      "China": "Ásia",
      "Chipre": "Europa",
      "Cingapura": "Ásia",
      "Cocos (Keeling), Ilhas": "Oceania",
      "Colômbia": "América do Sul",
      "Comores": "África",
      "Congo": "África",
      "Coreia, Republica Sul": "Ásia",
      "Costa do Marfim": "África",
      "Costa Rica": "América Central",
      "Croácia": "Europa",
      "Cuba": "América Central",
      "Curaçao": "América Central",
      "Dinamarca": "Europa",
      "Dominica": "América Central",
      "El Salvador": "América Central",
      "Emirados Arabes Unidos": "Ásia",
      "Equador": "América do Sul",
      "Eslovaca, Republica": "Europa",
      "Espanha": "Europa",
      "Estados Unidos": "América do Norte",
      "Estônia": "Europa",
      "Filipinas": "Ásia",
      "Finlândia": "Europa",
      "França": "Europa",
      "Gana": "África",
      "Gibraltar": "Europa",
      "Granada": "América Central",
      "Grécia": "Europa",
      "Guatemala": "América Central",
      "Guiana": "América do Sul",
      "Guiana Francesa": "América do Sul",
      "Guine Bissau": "África",
      "Guine Equatorial": "África",
      "Haiti": "América Central",
      "Honduras": "América Central",
      "Hong Kong": "Ásia",
      "Hungria": "Europa",
      "Ilha de Man": "Europa",
      "Ilhas Virgens": "América do Norte",
      "India": "Ásia",
      "Indonésia": "Ásia",
      "Irã": "Ásia",
      "Iraque": "Ásia",
      "Irlanda": "Europa",
      "Itália": "Europa",
      "Jamaica": "América Central",
      "Japão": "Ásia",
      "Jordânia": "Ásia",
      "Letônia": "Europa",
      "Líbano": "Ásia",
      "Libéria": "África",
      "Luxemburgo": "Europa",
      "Malásia": "Ásia",
      "Malta": "Europa",
      "Marshall, Ilhas": "Oceania",
      "Mauritânia": "África",
      "México": "América do Norte",
      "Moçambique": "África",
      "Montenegro": "Europa",
      "Namibia": "África",
      "Nicaragua": "América Central",
      "Nigéria": "África",
      "Noruega": "Europa",
      "Nova Caledônia": "Oceania",
      "Nova Zelândia": "Oceania",
      "Omã": "Ásia",
      "Países Baixos": "Europa",
      "Panamá": "América Central",
      "Paraguai": "América do Sul",
      "Peru": "América do Sul",
      "Polônia": "Europa",
      "Porto Rico": "América do Norte",
      "Portugal": "Europa",
      "Quênia": "África",
      "Reino Unido": "Europa",
      "República Dominicana": "América Central",
      "Rússia": "Europa/Ásia",
      "São Tomé e Príncipe": "África",
      "São Vicente e Granadinas": "América Central",
      "Senegal": "África",
      "Serra Leoa": "África",
      "Singapura": "Ásia",
      "Suazilândia": "África",
      "Suécia": "Europa",
      "Suíça": "Europa",
      "Suriname": "América do Sul",
      "Tailândia": "Ásia",
      "Taiwan (FORMOSA)": "Ásia",
      "Tanzânia": "África",
      "Tcheca, República": "Europa",
      "Togo": "África",
      "Trinidade Tobago": "América Central",
      "Tunísia": "África",
      "Turquia": "Europa/Ásia",
      "Tuvalu": "Oceania",
      "Uruguai": "América do Sul",
      "Vanuatu": "Oceania",
      "Venezuela": "América do Sul",
      "Vietnã": "Ásia"
}

df_total["continente"] = df_total["pais"].map(continentes_dic)

df_total["valor_medio_litro"] = df_total["valor"] / df_total["quantidade"]
df_total["valor_medio_litro"].fillna(0, inplace=True)

df_total = df_total[["ano", "pais_origem", "pais", "continente", "valor", "quantidade", "valor_medio_litro"]]

df_quinze = df_total.query("ano>=2008")

dolar_mes_ano = """Ano/Mês	Janeiro	Fevereiro	Março	Abril	Maio	Junho	Julho	Agosto	Setembro	Outubro	Novembro	Dezembro
1985	3.318,00	3.802,00	4.161,00	4.680,00	
1986	11.170,00	12.985,00	13,84	13,84	13,84	13,84	13,84	13,84	13,84	13,84	14,09	14,452
1987	15,589	17,985	20,729	23,820	30,874	38,097	44,918	46,931	49,719	53,016	58,026	67,423
1988	77,277	90,538	106,80	125,15	148,39	177,05	213,91	264,97	321,35	403,69	519,60	661,37
1989	859,25	1,00	1,00	1,00	1,10	1,3480	1,8820	2,4360	3,2190	4,3380	6,0480	9,1770
1990	13,735	24,345	38,388	46,853	51,239	55,962	66,531	71,982	75,493	92,477	118,24	151,31
1991	190,47	221,56	229,15	251,37	272,69	296,06	326,53	370,09	425,87	577,23	731,57	945,85
1992	1.179,05	1.467,45	1.768,45	2.196,00	2.612,80	3.144,10	3.789,80	4.620,45	5.697,40	7.118,10	8.872,30	11.066,95
1993	14.080,50	18.156,75	22.183,00	28.270,00	36.445,40	47.413,00	62.136,00	80.851,00	108,944	149,260	199,745	270,065
1994	381,530	532,660	755,520	1.104,88	1.508,820	2.230,00	0,925	0,906	0,855	0,835	0,838	0,851
1995	0,847	0,837	0,884	0,905	0,891	0,909	0,926	0,942	0,953	0,958	0,9627	0,9677
1996	0,97827	0,9829	0,9868	0,9899	0,9957	1,0015	1,0062	1,0122	1,0192	1,0251	1,0305	1,0389
1997	1,0426	1,0495	1,0554	1,0606	1,0678	1,0745	1,0808	1,0873	1,0927	1,0994	1,1082	1,1143
1998	1,1206	1,1276	1,1334	1,1407	1,1472	1,1551	1,1615	1,1716	1,1798	1,1886	1,1915	1,2052
1999	1,4659	1,8984	1,8825	1,6688	1,6570	1,7892	1,8281	1,8711	1,8779	1,9794	1,9331	1,8501
2000	1,7997	1,7764	1,7431	1,7833	1,8382	1,8079	1,8106	1,8056	1,8438	1,8764	1,9441	1,9678
2001	1,9475	1,9812	2,0864	2,1573	2,3384	2,4079	2,5538	2,5005	2,6986	2,7790	2,5299	2,3840
2002	2,3705	2,4380	2,3542	2,3180	2,5117	2,7181	2,8455	3,1912	3,1506	3,8567	3,6797	3,7342
2003	3,2983	3,6580	3,3958	3,1154	2,9306	2,8570	2,8554	2,9930	2,8898	2,8268	2,9418	2,9293
2004	2,8126	2,9085	2,9013	2,9064	3,0982	3,1380	3,0215	3,0235	2,9042	2,8623	2,7991	2,7508
2005	2,7074	2,5762	2,7621	2,5971	2,4715	2,4455	2,3427	2,3422	2,3012	2,2511	2,1990	2,2957
2006	2,2747	2,1375	2,1215	2,1426	2,1774	2,2845	2,2130	2.1480	2,1540	2,1419	2,1537	2,1470
2007	2,1407	2,0896	2,0909	2,0231	1,9922	1,9097	1,8684	2,0043	1,9031	1,8078	1,7378	1,7959
2008	1,7450	1,7541	1,6947	1,6822	1,6601	1,6368	1,5910	1,6389	1,8125	2,1551	2,2800	2,3690
2009	2,3803	2,2680	2,3012	2,1992	2,0762	1,9458	1,9420	1,8385	1,8087	1,7037	1,7290	1,7557
2010	1,7711	1,8670	1,7644	1,7483	1,7967	1,7971	1,7690	1,7716	1,7169	1,6604	1,7198	1,6988
2011	1,6843	1,6682	1,6692	1,5776	1,6328	1,5960	1,5743	1,5956	1,7106	1,7376	1,7649	1,8609
2012	1,7853	1,7158	1,8006	1,8364	1,9947	2,0443	2,0338	2,0234	2,0139	2,0382	2,0629	2,0840
2013	2,0374	1,9600	1,9749	1,9790	2,0233	2,1367	2,2548	2,3434	2,2785	2,1818	2,3289	2,3354
2014	2,3470	2,3924	2,3638	2,2257	2,2166	2,2347	2,2195	2,2690	2,3401	2,4316	2,6136	2,6717
2015	2,6122	2,8392	3,2264	3,0681	2,9894	3,1036	3,1532	3,4761	3,8599	3,8344	3,8023	3,8703
2016	3,8711	3,9885	3,7116	3,5276	3,5041	3,4768	3,2656	3,1672	3,3326	3,1864	3,4446	3,3830
2017	3,3830	3,2034	3,0779	3,1629	3,1269	3,1011	3,2836	3,1899	3,1976	3,1255	3,1572	3,2834
2018	3,3182	3,1963	3,2208	3,2859	3,4105	3,6753	3,7738	3,8745	3,9134	4,1879	3,7332	3,7924
2019	3,909	3,7049	3,7155	3,8344	3,8730	4,0031	3,8813	3,7463	4,0188	4,0616	4,1488	4,1831
2020	4,0949	4,1622	4,3163	4,7362	5,2579	5,8229	5,1883	5,3491	5,3852	5,2728	5,6172	5,4854
2021	5,0968	5,2714	5,3815	5,6296	5,6234	5,2701	5,0874	5,1000	5,2474	5,2576	5,4510	5,4199
2022	5,7127	5,5349	5,1881	5,1314	4,7158	5,1075	5,1119	5,4014	5,0925	5,2211	5,2824	5,3013"""
## Fonte direta: AASP (Associação de Advogados de São Paulo) - https://www.aasp.org.br/suporte-profissional/indices-economicos/mensal/dolar/
## Fonte indireta: SRF - Secretaria da Receita Federal

from io import StringIO

dolar_mes_ano_io = StringIO(dolar_mes_ano)

dolar = pd.read_csv(dolar_mes_ano_io, sep="\t")
dolar = dolar.dropna()
dolar = dolar.set_index("Ano/Mês")

dolar_dez = dolar["Dezembro"]
dolar_dez = dolar_dez.reset_index()
dolar_dez.rename(columns={"Ano/Mês": "ano", "Dezembro": "valor_dolar"}, inplace = True)
dolar_dez = dolar_dez.query("ano>=2008")

df_quinze = df_quinze.merge(dolar_dez, on="ano")

# TOTAL EXPORTADO POR ANO (Litros)
dados_por_ano = df_quinze[["ano", "valor", "quantidade"]]
dados_por_ano = dados_por_ano.groupby("ano").sum()
dados_por_ano["valor_med_litro"] = dados_por_ano["valor"] / dados_por_ano["quantidade"]

dados_por_ano = dados_por_ano.reset_index()


st.write("Teste")
ax = plt.figure(figsize=(10,5))
sns.scatterplot(x="ano", y="quantidade", data=dados_por_ano)
sns.lineplot(x="ano", y="quantidade", data=dados_por_ano, )
plt.title("Litros de Vinho Exportado por Ano")
plt.ylim(0, 30_000_000)
plt.xlabel("Ano")
plt.ylabel("Volume (Litros)")

st.plotly_chart(ax)
st.dataframe(dados_por_ano)
