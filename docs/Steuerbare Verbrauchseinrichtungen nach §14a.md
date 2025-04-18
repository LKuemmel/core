Der Gesetzgeber sieht verschiedene Möglichkeiten für steuerbare Verbrauchseinrichtungen vor. Für jede steuerbare Verbrauchseinrichtung kann eine andere Option angemeldet werden. Bei der Konfiguration muss deshalb auch immer der/die Ladepunkte angegeben werden, für die die IO-Aktion angewendet werden soll.

### Dimmen per EMS

Beim Dimmen wird eine maximale Bezugsleistung für alle steuerbaren Verbrauchseinrichtungen nach einer vorgegebene Formel ermittelt. Das Ergebnis dieser Formel muss bei der IO-Aktion `Dimmen` in der Einstellung `maximale Bezugsleistung` eingetragen werden. ACHTUNG: Die openWB kann aktuell nur die Ladepunkte berücksichtigen. Sind noch weitere steuerbare Verbraucher angemeldet, können diese über einen digitalen Ausgang angebunden werden. Da openWB die Leistung dieser Geräte nicht kennt, werden 4,2kW angenommen. Muss der Verbraucher seine Leistung begrenzen, wird der Ausgang auf 0V gesetzt. Für die korrekte Ermittlung der maximalen Bezugsleistung ist der Betreiber, nicht openWB oder die software2 verantwortlich.
Vorhandener Überschuss kann zusätzlich zur maximalen Bezugsleistung verwendet werden.

### Dimmung per Direkt-Steuerung

Bei der Dimmung per Direkt-Steuerung wird jede steuerbare Verbrauchseinrichtung separat angesteuert und ihr Leistungsbezug auf 4,2kW gedimmt.
Pro steuerbarer Verbrauchseinrichtung muss eine IO-Aktion konfiguriert werden und dort der Ladepunkt und der zugehörige Eingang angegeben werden.

### Rundsteuer-Empfänger-Kontakt (RSE)

Für den RSE-Kontakt kann ein Muster aus verschiedenen Eingängen und ein Prozentwert, auf den die Anschlussleistung begrenzt wird, angegeben werden.
