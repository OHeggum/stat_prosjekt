import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.formula.api as smf
import statsmodels.api as sm

df2 = pd.read_csv("datasett_filtrert.csv", sep=",", encoding="latin1")

# Enkel lineær regresjon
formel = 'Price ~ Pieces'

modell = smf.ols(formel, data = df2)
resultat = modell.fit()

print(resultat.summary())

fig, ax = plt.subplots(figsize=(12, 8))
slope = resultat.params['Pieces']
intercept = resultat.params['Intercept']

regression_x = np.array(df2['Pieces'])

regression_y = slope * regression_x + intercept

plt.scatter(df2['Pieces'], df2['Price'], label='Data Points')
plt.plot(regression_x, regression_y, color='red', label='Regression Line')

plt.xlabel('Antall brikker')
plt.ylabel('Pris [$]')
plt.title('Kryssplott med regresjonslinje (enkel LR)')
plt.legend()
plt.grid()
plt.show()

figure, axis = plt.subplots(1, 2, figsize = (15, 5))
sns.scatterplot(x = resultat.fittedvalues, y = resultat.resid, ax = axis[0])
axis[0].set_ylabel("Residual")
axis[0].set_xlabel("Predikert verdi")
axis[0].grid()

sm.qqplot(resultat.resid, line = '45', fit = True, ax = axis[1])
axis[1].set_ylabel("Kvantiler i residualene")
axis[1].set_xlabel("Kvantiler i normalfordelingen")

plt.grid()
plt.show()

# En modell for hver gruppe
formel = 'Price ~ Pieces'
df_with_theme = df2[df2['Theme_or_not'] == 'Yes']
df_without_theme = df2[df2['Theme_or_not'] == 'No']
df_unknown_theme = df2[df2['Theme_or_not']== 'Unknown']

modell_with_theme = smf.ols('Price ~ Pieces', data=df_with_theme).fit()
modell_without_theme = smf.ols('Price ~ Pieces', data=df_without_theme).fit()
modell_with_unknown_theme = smf.ols('Price ~ Pieces', data=df_unknown_theme).fit()

# Plot resultatene ved siden av hverandre
fig, axs = plt.subplots(1, 3, figsize=(16, 9))

# Plott for Lego med varemerke
axs[0].scatter(df_with_theme['Pieces'], df_with_theme['Price'], label='Data Points')
axs[0].plot(df_with_theme['Pieces'], modell_with_theme.predict(), color='red', label='Regression Line')
axs[0].set_xlabel('Antall brikker')
axs[0].set_ylabel('Pris [$]')
axs[0].set_title('Lego med varemerke')
axs[0].legend()

# Plott for Lego uten varemerke
axs[1].scatter(df_without_theme['Pieces'], df_without_theme['Price'], label='Data Points')
axs[1].plot(df_without_theme['Pieces'], modell_without_theme.predict(), color='red', label='Regression Line')
axs[1].set_xlabel('Antall brikker')
axs[1].set_ylabel('Pris [$]')
axs[1].set_title('Lego uten varemerke')
axs[1].legend()

# Plott for Lego med ukjent varemerke
axs[2].scatter(df_unknown_theme['Pieces'], df_unknown_theme['Price'], label='Data Points')
axs[2].plot(df_unknown_theme['Pieces'], modell_with_unknown_theme.predict(), color='red', label='Regression Line')
axs[2].set_xlabel('Antall brikker')
axs[2].set_ylabel('Pris [$]')
axs[2].set_title('Lego med ukjent varemerke')
axs[2].legend()

plt.tight_layout()
plt.show()

print(modell_with_theme.summary())
print(modell_without_theme.summary())
print(modell_with_unknown_theme.summary())

# Opprett dummyvariabler for hvert tema
df2['Is_Theme'] = np.where(df2['Theme_or_not'] == 'Yes', 1, np.where(df2['Theme_or_not'] == 'No', 0, 2))

# Lineær regresjon med separate skjæringspunkter for hver gruppe
modell = smf.ols('Price ~ Pieces + Is_Theme', data=df2).fit()

fig, ax = plt.subplots(figsize=(12, 8))
# Plot resultatene
plt.scatter(df2[df2['Theme_or_not']=='Yes']['Pieces'], df2[df2['Theme_or_not']=='Yes']['Price'], color='blue', label='Data Points - With Theme')
plt.scatter(df2[df2['Theme_or_not']=='No']['Pieces'], df2[df2['Theme_or_not']=='No']['Price'], color='red', label='Data Points - Without Theme')
plt.scatter(df2[df2['Theme_or_not']=='Unknown']['Pieces'], df2[df2['Theme_or_not']=='Unknown']['Price'], color='green', label='Data Points - Unknown Theme')

plt.plot(df2[df2['Theme_or_not']=='Yes']['Pieces'], modell.predict(df2[df2['Theme_or_not']=='Yes']), color='blue', label='Regression Line - With Theme')
plt.plot(df2[df2['Theme_or_not']=='No']['Pieces'], modell.predict(df2[df2['Theme_or_not']=='No']), color='red', label='Regression Line - Without Theme')
plt.plot(df2[df2['Theme_or_not']=='Unknown']['Pieces'], modell.predict(df2[df2['Theme_or_not']=='Unknown']), color='green', label='Regression Line - Unknown Theme')

plt.xlabel('Antall brikker')
plt.ylabel('Pris [$]')
plt.title('Lineær regresjon med separate skjæringspunkter')
plt.legend()
plt.grid()
plt.show()

# Skriv ut modellinformasjonen
print(modell.summary())

# Modell med interaksjonsledd
modell_interact = smf.ols('Price ~ Pieces * Theme_or_not', data=df2).fit()

fig, ax = plt.subplots(figsize=(12, 8))

# Plot resultatene
# Endre fargen på plottene til grønn
plt.scatter(df2[df2['Theme_or_not']=='Yes']['Pieces'], df2[df2['Theme_or_not']=='Yes']['Price'], color='blue', label='Varemerke')
plt.scatter(df2[df2['Theme_or_not']=='No']['Pieces'], df2[df2['Theme_or_not']=='No']['Price'], color='red', label='Ikke varemerke')
plt.scatter(df2[df2['Theme_or_not']=='Unknown']['Pieces'], df2[df2['Theme_or_not']=='Unknown']['Price'], color='green', label='Ukjent varemerke')


# Legg til regresjonslinje for Lego med varemerke
plt.plot(df2[df2['Theme_or_not']=='Yes']['Pieces'], modell_interact.predict(df2[df2['Theme_or_not']=='Yes']), color='blue', label='Regresjonslinje - Varemerke')

# Legg til regresjonslinje for Lego uten varemerke
plt.plot(df2[df2['Theme_or_not']=='No']['Pieces'], modell_interact.predict(df2[df2['Theme_or_not']=='No']), color='red', label='Regresjonslinje - Ikke varemerke')

# Legg til regresjonslinje for Lego med ukjent varemerke
plt.plot(df2[df2['Theme_or_not']=='Unknown']['Pieces'], modell_interact.predict(df2[df2['Theme_or_not']=='Unknown']), color='green', label='Regresjonslinje - Ukjent varemerke')

plt.xlabel('Antall brikker')
plt.ylabel('Pris [$]')
plt.title('Multippel lineær regresjon med interaksjonseffekt')
plt.legend()
plt.grid()
plt.show()

# Skriv ut modellinformasjonen
print(modell_interact.summary())


