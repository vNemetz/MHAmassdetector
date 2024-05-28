import matplotlib.pyplot as plot
import numpy as np
import pandas as pan
from scipy.optimize import curve_fit
import seaborn as sb

# define a função posição do movimento harmônico amortecido
def funcao(t, A, b, w,phi):
    return A * np.exp(-b * t)* np.cos((w * t) - phi)

#cria uma lista com os dados do arquivo .csv
dados = pan.read_csv("dados.csv")

# transforma a posição de pixels para metros
dados["posicao(m)"] *= 0.175/((np.max(dados["posicao(m)"] + np.min(dados["posicao(m)"])))/2)
# subtrai a amplitude da posição em pixels, deixando o valor 0 como a posição de equilíbrio
dados["posicao(m)"] -= ((np.max(dados["posicao(m)"] + np.min(dados["posicao(m)"])))/2)


#calcula os parâmetros da função do MHA na ordem: A, b, w, phi com base nos dados e na função
parametros = curve_fit(funcao, dados["t(s)"],dados["posicao(m)"])[0]
print("A: ",parametros[0], "b: ", parametros[1], "w: ", parametros[2], "phi: ", parametros[3])

# usa os parâmetros para criar uma linearização dos dados
dados["fit"] = funcao(dados["t(s)"],*parametros)

# calcula o fator de qualidade do sistema
fatordeQualidade=parametros[2]/(2 * parametros[1])
print("Fator de Qualidade: ", fatordeQualidade)

# plota e mostra os gráficos
sb.scatterplot(dados,x="t(s)",y="posicao(m)")
sb.lineplot(dados,x="t(s)",y="fit")
plot.show()     












#fatordeQualidade = 2*(np.pi)/(1-np.exp(-2 * parametros[1] * periodo))
#print(fatordeQualidade)