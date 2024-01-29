import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import plotly.express as px
import plotly.figure_factory as ff



dados = pd.read_csv(r'ExpVinho 2022.csv', encoding='UTF-8', engine='python', sep=';', thousands='.', decimal=',')
#pd.options.display.float_format = '{:,.2f}'.format

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

df_total = df_total[df_total["quantidade"] != 0]
df_total = df_total.sort_values(by="ano", ascending=True)
df_total = df_total.reset_index()
df_total.head()


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
df_valormed_quinze = dados_por_ano["valor"].sum() / dados_por_ano["quantidade"].sum()

dados_por_ano = dados_por_ano.reset_index()


met_quantidade = dados_por_ano["quantidade"].sum()
met_valor = dados_por_ano["valor"].sum()

media_valor = dados_por_ano["valor"].sum() / 15
media_quantidade = dados_por_ano["quantidade"].sum() / 15

def formata_numero(valor, prefixo=""):
    for unidade in ["", "mil"]:
        if valor <1000:
            return f'{prefixo} {valor:,.2f} {unidade}'
        valor /= 1000
    return f'{prefixo} {valor:,.2f} MM'


# TABELA COM LONGITUDE E LATITUDE
lat = {
"Afeganistão": 33.93911,
"África do Sul": -30.5595,
"Alemanha, República Democrática": 51.1657,
"Angola": -8.81155,
"Anguilla": 18.2206,
"Antígua e Barbuda": 17.0608,
"Antilhas Holandesas": 12.2261,
"Argentina": -38.4161,
"Aruba": 12.5211,
"Austrália": -25.2744,
"Áustria": 47.5162,
"Bahamas": 25.0343,
"Bangladesh": 23.685,
"Barbados": 13.1939,
"Barein": 25.9304,
"Bélgica": 50.5039,
"Belice": 17.1899,
"Benin": 9.3077,
"Bolívia": -16.2902,
"Bósnia-Herzegovina": 43.9159,
"Brasil": -14.235,
"Bulgária": 42.7339,
"Cabo Verde": 16.5388,
"Camarões": 7.3697,
"Canadá": 56.1304,
"Catar": 25.3548,
"Cayman, Ilhas": 19.3133,
"Chile": -35.6751,
"China": 35.8617,
"Chipre": 35.1264,
"Cingapura": 1.3521,
"Cocos (Keeling), Ilhas": -12.1642,
"Colômbia": 4.5709,
"Comores": -11.6455,
"Congo": -4.0383,
"Coreia, Republica Sul": 35.9078,
"Costa do Marfim": 7.539,
"Costa Rica": 9.7489,
"Croácia": 45.1,
"Cuba": 21.5218,
"Curaçao": 12.1696,
"Dinamarca": 56.2639,
"Dominica": 15.415,
"El Salvador": 13.7942,
"Emirados Arabes Unidos": 23.4241,
"Equador": -1.8312,
"Eslovaca, Republica": 48.669,
"Espanha": 40.4637,
"Estados Unidos": 37.0902,
"Estônia": 58.5953,
"Filipinas": 12.8797,
"Finlândia": 61.9241,
"França": 46.6034,
"Gana": 7.9465,
"Gibraltar": 36.1408,
"Granada": 12.1165,
"Grécia": 39.0742,
"Guatemala": 15.7835,
"Guiana": 4.8604,
"Guiana Francesa": 3.9339,
"Guine Bissau": 11.8037,
"Guine Equatorial": 1.6508,
"Haiti": 18.9712,
"Honduras": 15.2,
"Hong Kong": 22.3193,
"Hungria": 47.1625,
"Ilha de Man": 54.2361,
"Ilhas Virgens": 18.3358,
"India": 20.5937,
"Indonésia": -0.7893,
"Irã": 32.4279,
"Iraque": 33.2232,
"Irlanda": 53.4129,
"Itália": 41.8719,
"Jamaica": 18.1096,
"Japão": 36.2048,
"Jordânia": 30.5852,
"Letônia": 56.8796,
"Líbano": 33.8547,
"Libéria": 6.4281,
"Luxemburgo": 49.8153,
"Malásia": 4.2105,
"Malta": 35.9375,
"Marshall, Ilhas": 7.1315,
"Mauritânia": 21.0079,
"México": 23.6345,
"Moçambique": -18.6657,
"Montenegro": 42.7087,
"Namibia": -22.9576,
"Nicaragua": 12.8654,
"Nigéria": 9.082,
"Noruega": 60.472,
"Nova Caledônia": -20.9043,
"Nova Zelândia": -40.9006,
"Omã": 21.4735,
"Países Baixos": 52.1326,
"Panamá": 8.5379,
"Paraguai": -23.4425,
"Peru": -9.19,
"Polônia": 51.9194,
"Porto Rico": 18.2208,
"Portugal": 39.3999,
"Quênia": -0.0236,
"Reino Unido": 55.3781,
"República Dominicana": 18.7357,
"Rússia": 61.524,
"São Tomé e Príncipe": 0.1864,
"São Vicente e Granadinas": 12.9843,
"Senegal": 14.4974,
"Serra Leoa": 8.4606,
"Singapura": 1.3521,
"Suazilândia": -26.5225,
"Suécia": 60.1282,
"Suíça": 46.8182,
"Suriname": 3.9193,
"Tailândia": 15.870,
"Taiwan (FORMOSA)": 23.6978,
"Tanzânia": -6.369,
"Tcheca, República": 49.8175,
"Togo": 8.6195,
"Trinidade Tobago": 10.6918,
"Tunísia": 33.8869,
"Turquia": 38.9637,
"Tuvalu": -7.1095,
"Uruguai": -32.5228,
"Vanuatu": -15.376,
"Venezuela": 6.4238,
"Vietnã": 14.0583
}

lon = {
"Afeganistão": 67.709953,
"África do Sul": 22.9375,
"Alemanha, República Democrática": 10.4515,
"Angola": 17.8739,
"Anguilla": -63.0686,
"Antígua e Barbuda": -61.7964,
"Antilhas Holandesas": -68.2997,
"Argentina": -63.6167,
"Aruba": -69.9683,
"Austrália": 133.7751,
"Áustria": 14.5501,
"Bahamas": -77.3963,
"Bangladesh": 90.3563,
"Barbados": -59.5432,
"Barein": 50.6378,
"Bélgica": 4.4699,
"Belice": -88.4976,
"Benin": 2.3158,
"Bolívia": -63.5887,
"Bósnia-Herzegovina": 17.6791,
"Brasil": -51.9253,
"Bulgária": 25.4858,
"Cabo Verde": -23.0418,
"Camarões": 12.3547,
"Canadá": -106.3468,
"Catar": 51.1839,
"Cayman, Ilhas": -81.2546,
"Chile": -71.5429,
"China": 104.1954,
"Chipre": 33.4299,
"Cingapura": 103.8198,
"Cocos (Keeling), Ilhas": 96.8705,
"Colômbia": -74.2973,
"Comores": 43.8722,
"Congo": 21.7587,
"Coreia, Republica Sul": 127.7669,
"Costa do Marfim": -5.5471,
"Costa Rica": -84.204,
"Croácia": 15.2000,
"Cuba": -77.7812,
"Curaçao": -68.9900,
"Dinamarca": 9.5018,
"Dominica": -61.371,
"El Salvador": -88.8965,
"Emirados Arabes Unidos": 53.8478,
"Equador": -78.1834,
"Eslovaca, Republica": 19.0402,
"Espanha": -3.7492,
"Estados Unidos": -95.7129,
"Estônia": 25.0136,
"Filipinas": 121.774,
"Finlândia": 25.7482,
"França": 1.4429,
"Gana": -1.0232,
"Gibraltar": -5.3536,
"Granada": -61.679,
"Grécia": 21.8243,
"Guatemala": -90.2308,
"Guiana": -58.9302,
"Guiana Francesa": -53.1258,
"Guine Bissau": -15.1804,
"Guine Equatorial": 10.2679,
"Haiti": -72.2852,
"Honduras": -86.2419,
"Hong Kong": 114.1694,
"Hungria": 19.5033,
"Ilha de Man": -4.5481,
"Ilhas Virgens": -64.8963,
"India": 78.9629,
"Indonésia": 113.9213,
"Irã": 53.6880,
"Iraque": 43.6793,
"Irlanda": -8.2439,
"Itália": 12.4964,
"Jamaica": -77.2975,
"Japão": 138.2529,
"Jordânia": 36.2384,
"Letônia": 24.6032,
"Líbano": 35.8623,
"Libéria": -9.4295,
"Luxemburgo": 6.1296,
"Malásia": 101.9758,
"Malta": 14.3754,
"Marshall, Ilhas": 171.1845,
"Mauritânia": -10.9408,
"México": -102.5528,
"Moçambique": 35.5296,
"Montenegro": 19.3744,
"Namibia": 18.4904,
"Nicaragua": -85.2072,
"Nigéria": 8.6753,
"Noruega": 8.4689,
"Nova Caledônia": 165.6180,
"Nova Zelândia": 174.8860,
"Omã": 55.9233,
"Países Baixos": 5.2913,
"Panamá": -80.7821,
"Paraguai": -58.4438,
"Peru": -75.0152,
"Polônia": 19.1451,
"Porto Rico": -66.5901,
"Portugal": -8.2245,
"Quênia": 37.9062,
"Reino Unido": -3.4360,
"República Dominicana": -70.1627,
"Rússia": 105.3197,
"São Tomé e Príncipe": 6.6131,
"São Vicente e Granadinas": -61.2872,
"Senegal": -14.4524,
"Serra Leoa": -11.7799,
"Singapura": 103.8198,
"Suazilândia": 31.4659,
"Suécia": 18.6435,
"Suíça": 8.2275,
"Suriname": -56.0278,
"Tailândia": 100.9925,
"Taiwan (FORMOSA)": 120.9605,
"Tanzânia": 34.8888,
"Tcheca, República": 15.4729,
"Togo": 0.8248,
"Trinidade Tobago": -61.2225,
"Tunísia": 9.5375,
"Turquia": 35.2433,
"Tuvalu": 177.6493,
"Uruguai": -55.7658,
"Vanuatu": 166.9592,
"Venezuela": -66.5897,
"Vietnã": 108.2772
}

df_total["lat"] = df_total["pais"].map(lat)
df_total["lon"] = df_total["pais"].map(lon)

topvalor = df_quinze[["pais", "valor", "quantidade"]].groupby(['pais']).sum().sort_values("valor", ascending=False).reset_index()
topvalor = topvalor.head()

topvol = df_quinze[["pais", "valor", "quantidade"]].groupby(['pais']).sum().sort_values("quantidade", ascending=False).reset_index()
topvol = topvol.head()

toppreco = df_quinze[["pais", "valor", "quantidade"]].groupby(['pais']).sum().reset_index()
fil_toppreco = toppreco[toppreco["pais"].isin(["Rússia", "Paraguai", "Estados Unidos"])]
fil_toppreco["preco_medio"] = fil_toppreco["valor"] / fil_toppreco["quantidade"]
fil_toppreco = fil_toppreco.sort_values("preco_medio", ascending=True)
fil_toppreco = fil_toppreco.head(3)
    
## GRAFICO MAPA
##receita_dados = df_quinze.groupby("pais")[['valor']].sum()
##receita_dados = df_quinze.drop_duplicates(subset='pais')[["pais", "lat", "lon"]].merge(df_quinze, left_on="pais", right_index=True).sort_values("valor", ascending=False)

##### INÍCIO DO DASHBOARD #####

st.set_page_config(page_title="Tech Challenge 01 - Gio Queiroz", page_icon=":wine_glass:", layout="wide", initial_sidebar_state="auto", menu_items=None)

# CABEÇALHO
st.markdown(
        """
    <style>
    .title-style {
        text-align: left;
        font-weight: bold;
        color: #962450;
        font-size: 40px;
    }

    .subtitle-style {
        text-align: left;
        font-weight: bold;
        color: #737373;
        font-size: 40px;
    }

    .about-style {
        font-weight: bold;
        color: #d93474;
    }

     .about2-style {
        font-weight: normal;
        color: #000000;
    }

    .about3-style {
        font-weight: bold;
        color: #000000;
    }

    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 16px;
        font-weight: normal;
    }

    .button:hover {
        font-size: 16px;
        font-weight: normal;
        color: red;
    }

	.stTabs [data-baseweb="tab"] {
		height: 50px;
        white-space: pre-wrap;
		border-radius: 4px 4px 0px 0px;
		gap: 1px;
		padding-top: 10px;
		padding-bottom: 10px;
    }

    .tab1-title {
        font-weight: bold;
        font-size: 30px;
        color: #962450;
    }

    [data-testid="stMetric"] {
        background-color: #e8e8e8;
        border-radius: 10px;
        text-align: left;
        font-weight: bold;
        color: #962450;
        padding: 5% 5% 5% 5%;
        font-size: 40px;
        border-style: groove;
        border-width: 1px;
        border-color: #962450;
    }
}
    </style>
    """,
        unsafe_allow_html=True,
    )
st.markdown('<p class="title-style">MaWine: <h n class="subtitle-style">Exportação de Vinhos de Mesa</h></p>', unsafe_allow_html=True)
st.write("Bem-vindo ao relatório de exportação de vinhos da MaWine.")

st.markdown(':wine_glass:<h class="about-style"> Sobre a empresa: <h n class="about2-style">A MaWine é uma produtora e distribuidora de vinhos situada no Nordeste do Brasil. Fundada em 1970, oferece uma variedade rótulos de vinhos para diversos clientes ao redor do mundo.</h>', unsafe_allow_html=True)
st.markdown(':male-office-worker:<h class="about-style"> Sobre o time responsável: <h n class="about2-style">Somos Experts em Data Analytics e fazemos parte do DataTeam da MaWine.</h>', unsafe_allow_html=True)

st.markdown('<p class="about-style">Objetivos do Relatório:</p>', unsafe_allow_html=True)
st.markdown("- Apresentar aos investidores e acionistas o montante de venda de exportação da MaWine nos últimos 15 anos, separando a análise por país e trazendo prospecções futuras e ações para uma melhoria nas exportações.")

st.markdown('<p class="about-style">Metodologia</p>', unsafe_allow_html=True)
st.markdown("- Utilizando o python e suas bibliotecas, fizemos a aquisição, a manipulação e o tratamento dos dados obtidos na fonte, assim como utilizamos gráficos para permitir a visualização e compreensão desses dados.")

st.markdown('<p class="about3-style">Fonte de Dados: <a href="http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_06" class="about2-style">Dados da Vitivinicultura - Embrapa</p>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs([":bar_chart: Dados de Exportação", ":clipboard: Tabela (Origem x Destino)", ":chart: Análise Final"])
tab1.write()
tab2.write()
tab3.write()
with tab1:
    st.markdown('<p class="tab1-title">Resultados Gerais de Exportação</p>', unsafe_allow_html=True)
    
    coluna1, coluna2, coluna3 = st.columns(3)
    with coluna1:
        st.metric("Volume Total Exportado (L)", formata_numero(met_quantidade))
    with coluna2:
        st.metric("Valor Total Exportado (US$)", formata_numero(met_valor, 'US$'))
    with coluna3:
        st.metric("Preço Médio do Litro (US$)", formata_numero(df_valormed_quinze, 'US$'))
    st.markdown("Resumo com período")


    st.markdown("""---""")
    st.markdown('<p class="tab1-title">Total de Exportação - Ano a Ano</p>', unsafe_allow_html=True)

    coluna4, coluna5 = st.columns(2)
    with coluna4:
        option = st.selectbox(
        'Selecione o dado:',
        ('Valor Exportado por Ano (US$)', 'Volume Exportado por Ano (Litros)'))

        if option == "Valor Exportado por Ano (US$)":
            ax = px.bar(dados_por_ano, x="ano", y="valor", color_discrete_sequence=['#c43366'], width=800, height=500, range_x=[2007, 2023], range_y=[0, 25_000_000], title="Valor Exportado por Ano (US$)")
            ax.update_xaxes(dtick=1)
            ax.update_layout(
            yaxis=dict(
            title="Valor Exportado (US$)",
            titlefont=dict(size=16),
            tickfont=dict(size=14),
            showgrid=True,
            gridcolor="#c2c0c0",
            griddash="dash",
            title_standoff=20 # The higher the value, the farther away it is displayed
            ),
            xaxis = dict(
            title="Ano",
            tickmode = 'array',
            tickvals = [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
            titlefont=dict(size=16),
            tickfont=dict(size=14),
            tickangle=-45,
            title_standoff=20 # The higher the value, the farther away it is displayed
            ))
            ax.add_hline(y=media_valor, line_color="black", line_width=1, line_dash="dot", label=dict(text="                                                                  Valor Médio: US$ 7,51 MM", textposition="middle", font=dict(size=14, color="black"))
            )
            st.plotly_chart(ax, use_container_width=True)

        elif option == "Volume Exportado por Ano (Litros)":
            bx = px.bar(dados_por_ano, x="ano", y="quantidade", color_discrete_sequence=['#c43366'], width=800, height=500, range_x=[2007, 2023], range_y=[0, 25_000_000], title="Volume Exportado por Ano (Litros)")
            bx.update_xaxes(dtick=1)
            bx.update_layout(
            yaxis=dict(
            title="Valor Exportado (US$)",
            titlefont=dict(size=16),
            tickfont=dict(size=14),
            showgrid=True,
            gridcolor="#c2c0c0",
            griddash="dash",
            title_standoff=20 # The higher the value, the farther away it is displayed
            ),
            xaxis = dict(
            title="Ano",
            tickmode = 'array',
            tickvals = [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
            titlefont=dict(size=16),
            tickfont=dict(size=14),
            tickangle=-45,
            title_standoff=20 # The higher the value, the farther away it is displayed
            ))
            bx.add_hline(y=media_quantidade, line_color="black", line_width=1, line_dash="dot", label=dict(text="                                                           Volume Médio: 5,87 MM litros", textposition="middle", font=dict(size=14, color="black"))
            )
            st.plotly_chart(bx, use_container_width=True)

    with coluna5:
        st.write("Relatório")
   
    st.markdown("""---""")
    st.markdown('<p class="tab1-title">Países: Maiores Importadores da MaWine</p>', unsafe_allow_html=True)

    coluna6, coluna7 = st.columns(2)
    
    with coluna6:
        st.write("Relatório")
    
    with coluna7:
        option = st.selectbox(
        'Selecione o dado:',
        ('Valor Exportado por País (US$)', 'Volume Exportado por País (Litros)', 'Preço Médio (US$/L)'))

        if option == "Valor Exportado por País (US$)":
            ax = px.bar(topvalor, x="pais", y="valor", color_discrete_sequence=['#c43366'], width=800, height=500, range_y=[0, 41_000_000], title="Top 5 Países - Valor Exportado (US$) - Período: 2008 a 2022")
            ax.update_xaxes(dtick=1)
            ax.update_layout(
            yaxis=dict(
            title="Valor Exportado (US$)",
            titlefont=dict(size=16),
            tickfont=dict(size=14),
            showgrid=True,
            gridcolor="#c2c0c0",
            griddash="dash",
            title_standoff=20 # The higher the value, the farther away it is displayed
            ),
            xaxis = dict(
            title="Ano",
            tickmode = 'array',
            titlefont=dict(size=16),
            tickfont=dict(size=14),
            title_standoff=20 # The higher the value, the farther away it is displayed
            ))

            st.plotly_chart(ax, use_container_width=True)

        elif option == "Volume Exportado por País (Litros)":
            bx = px.bar(topvol, x="pais", y="quantidade", color_discrete_sequence=['#c43366'], width=800, height=500, range_y=[0, 41_000_000], title="Top 5 Países - Volume Exportado (Litros) - Período: 2008 a 2022")
            bx.update_xaxes(dtick=1)
            bx.update_layout(
            yaxis=dict(
            title="Volume Exportado (Litros)",
            titlefont=dict(size=16),
            tickfont=dict(size=14),
            showgrid=True,
            gridcolor="#c2c0c0",
            griddash="dash",
            title_standoff=20 # The higher the value, the farther away it is displayed
            ),
            xaxis = dict(
            title="Ano",
            tickmode = 'array',
            titlefont=dict(size=16),
            tickfont=dict(size=14),
            title_standoff=20 # The higher the value, the farther away it is displayed
            ))
            st.plotly_chart(bx, use_container_width=True)

        elif option == "Preço Médio (US$/L)":
            cx = px.bar(fil_toppreco, x="pais", y="quantidade", color_discrete_sequence=['#c43366'], width=800, height=500, range_y=[0, 41_000_000], title="Top 3 Países - Preço Médio do Litro de Vinho (US$/L) - Período: 2008 a 2022")
            cx.update_xaxes(dtick=1)
            cx.update_layout(
            yaxis=dict(
            title="Preço Médio (US$/L)",
            titlefont=dict(size=16),
            tickfont=dict(size=14),
            showgrid=True,
            gridcolor="#c2c0c0",
            griddash="dash",
            title_standoff=30 # The higher the value, the farther away it is displayed
            ),
            xaxis = dict(
            title="Ano",
            tickmode = 'array',
            titlefont=dict(size=16),
            tickfont=dict(size=14),
            title_standoff=30 # The higher the value, the farther away it is displayed
            ))
            st.plotly_chart(cx, use_container_width=True)
        
    st.markdown("""---""")
    st.markdown('<p class="tab1-title">Países: Top 3 - Observando de Perto</p>', unsafe_allow_html=True)

    option = st.selectbox(
        'Selecione o dado:',
        ('Paraguai', 'Rússia', 'Estados Unidos'))

    if option == "Paraguai":
            ax = px.bar(topvalor, x="pais", y="valor", color_discrete_sequence=['#c43366'], width=800, height=500, range_y=[0, 41_000_000], title="Top 5 Países - Valor Exportado (US$) - Período: 2008 a 2022")
            ax.update_xaxes(dtick=1)
            ax.update_layout(
            yaxis=dict(
            title="Valor Exportado (US$)",
            titlefont=dict(size=16),
            tickfont=dict(size=14),
            showgrid=True,
            gridcolor="#c2c0c0",
            griddash="dash",
            title_standoff=30 # The higher the value, the farther away it is displayed
            ),
            xaxis = dict(
            title="Ano",
            tickmode = 'array',
            titlefont=dict(size=16),
            tickfont=dict(size=14),
            title_standoff=30 # The higher the value, the farther away it is displayed
            ))

            st.plotly_chart(ax, use_container_width=True)

    elif option == "Rússia":
            bx = px.bar(topvol, x="pais", y="quantidade", color_discrete_sequence=['#c43366'], width=800, height=500, range_y=[0, 41_000_000], title="Top 5 Países - Volume Exportado (Litros) - Período: 2008 a 2022")
            bx.update_xaxes(dtick=1)
            bx.update_layout(
            yaxis=dict(
            title="Volume Exportado (Litros)",
            titlefont=dict(size=16),
            tickfont=dict(size=14),
            showgrid=True,
            gridcolor="#c2c0c0",
            griddash="dash",
            title_standoff=30 # The higher the value, the farther away it is displayed
            ),
            xaxis = dict(
            title="Ano",
            tickmode = 'array',
            titlefont=dict(size=16),
            tickfont=dict(size=14),
            title_standoff=30 # The higher the value, the farther away it is displayed
            ))
            st.plotly_chart(bx, use_container_width=True)

    elif option == "Estados Unidos":
            cx = px.bar(fil_toppreco, x="pais", y="quantidade", color_discrete_sequence=['#c43366'], width=800, height=500, range_y=[0, 41_000_000], title="Top 3 Países - Preço Médio do Litro de Vinho (US$/L) - Período: 2008 a 2022")
            cx.update_xaxes(dtick=1)
            cx.update_layout(
            yaxis=dict(
            title="Preço Médio (US$/L)",
            titlefont=dict(size=16),
            tickfont=dict(size=14),
            showgrid=True,
            gridcolor="#c2c0c0",
            griddash="dash",
            title_standoff=30 # The higher the value, the farther away it is displayed
            ),
            xaxis = dict(
            title="Ano",
            tickmode = 'array',
            titlefont=dict(size=16),
            tickfont=dict(size=14),
            title_standoff=30 # The higher the value, the farther away it is displayed
            ))
            st.plotly_chart(cx, use_container_width=True)

with tab2:
    df_display = df_total
    df_display["ano"] = df_display["ano"].map('{:.0f}'.format)
    df_display["valor"] = df_display["valor"].map('$ {:,.0f}'.format)
    df_display["quantidade"] = df_display["quantidade"].map('{:,.0f}'.format)
    df_display["valor_medio_litro"] = df_display["valor_medio_litro"].map('$ {:,.2f}'.format)
    df_display = df_display.rename(columns={
        "ano": "Ano", 
        "pais_origem": "País de Origem",
        "pais": "País de Destino",
        "continente": "Continente", 
        "valor": "Valor Exportado (US$)", 
        "quantidade": "Volume Exportado (Litros)", 
        "valor_medio_litro": "Preço (U$/Litro)",
        "lat": "Latitude",
        "lon": "Longitude"
        }
    )
    st.dataframe(df_display)

#with tab3:
    ## GRAFICO MAPA
    #df_mapa = df_total.groupby("pais")[['valor']].sum()
    #df_mapa = df_total.drop_duplicates(subset='pais')[["pais", "lat", "lon"]].merge(df_total, left_on="pais", right_index=True).sort_values("valor", ascending=False)

    #fig_mapa_receita = px.scatter_geo(df_mapa,
    #                                  lat='lat',
    #                                  lon='lon',
    #                                  size='valor',
    #                                  template='seaborn',
    #                                  hover_name='pais',
    #                                  hover_data={'lat':False, 'lon':False},
    #                                  title='Valor (US$) de Exportação por País')
    #st.plotly_chart(fig_mapa_receita)
