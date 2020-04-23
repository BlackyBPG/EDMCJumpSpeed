# JumpSpeed EDMC Plugin

Das ist ein einfaches Plugin f�r den [ED MarketConnector](https://github.com/Marginal/EDMarketConnector/wiki), basierend auf dem Original [EDMCJumpSpeed](https://github.com/Exynom/EDMC-HourlyIncome) vom inorton!

![In-game Screenshot](edmc_plugins_jsd.png)

![In-game Screenshot](edmc_plugins_light.png) ![In-game Screenshot](edmc_plugins_dark.png)


## Installation

So wie auch alle anderen EDMC-Plugins wird der Ordner aus dem heruntergeladenen Archiv in den Plugin-Ordner eures EDMC's entpackt, das sollte danach dann in etwa so aussehen:
```
$AppPath$\EDMarketConnector\plugins\JumpSpeed
```
Nach dem starten des EDMC ist das Plugin sofort einsatzbereit, es ist bereits kompatibel mit der neuen BETA-Version des EDMC 3.50 beta0, funktioniert jedoch auch in der Version 3.43 des EDMC.


## Anzeigen

Es wird folgendes im Plugin angezeigt:

- Zeile 1:
- - Links: Spr�nge pro Stunde dieser Sitzung
- - Rechts: Spr�nge pro Stunde gesamte Spielzeit
- Zeile 2:
- - Links: Sprungdistanz pro Stunde dieser Sitzung
- - Rechts: Sprungdistanz pro Stunde gesamte Spielzeit
- Zeile 3:
- - Links: Gesamtdistanz dieser Sitzung
- - Rechts: Gesamtdistanz gesamte Spielzeit

Die Zeit die ein Profil gespielt wurde sowie aktuelle Sprungdistanz und die Anzahl der durchgef�hrten Spr�nge wird beim Laden des Spieles (also EDMC vorher starten) abgefragt.


## Wichtiges

Das Plugin erkennt nicht automatisch welches Design (Theme) man in EDMC aktiviert hat, weshalb es eine Optionsseite mit der m�glichkeit der Designwahl f�r das Plugin gibt.

![EDMC Optionen](edmc_options_jumpspeed.png)


## Weiteres

Dieses Plugin ist lediglich f�r eigene statistische Auswertungen gedacht und synchronisiert sich selbst in keinster Weise mit irgendwelchen anderen Plattformen.
F�r jene welche in anderen Sprachen spielen ist es m�glich weitere �bersetzungsdateien an zu legen, diese kommen dann ebenso wie die deutsche �bersetzung in den L10n Ordner innerhalb des Plugin-Ordners.
