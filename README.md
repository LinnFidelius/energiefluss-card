# Energiefluss Card

Eine Home-Assistant-Karte, die den Energiefluss übersichtlich zeigt: PV oben, Netz links, Akku rechts, Haus unten und eine Wallbox, sobald sie lädt. Die Symbole sind isometrische 3D-Bilder, die Linien zeigen nur aktive Flüsse mit langsamer, leistungsabhängiger Animation.

<img src="docs/vorschau.gif" width="49%" alt="Vorschau 3D"> <img src="docs/vorschau-2d.gif" width="49%" alt="Vorschau 2D mit allen Verbrauchern">

Die Vorschau klappt die Verbraucherliste automatisch auf und wieder zu.


## Funktionen

- Fluss-Berechnung aus PV-, Netz-, Akku- und Haussensoren (PV deckt zuerst das Haus, dann den Akku, der Rest geht ins Netz)
- Netz: Bezug rot, Einspeisung grün, Vorzeichen umkehrbar oder getrennte Bezug-/Einspeise-Sensoren
- Akku mit Ladestand, Restlaufzeit („bis 06:40“) aus Kapazität und Mindest-SoC; Entladeleistung über die laufende Entladephase gemittelt (Standard max. 60 min, `runtime_window`), Uhrzeit auf 10 min gerundet
- Ladezeit beim Laden („voll ca. 13:10“ bzw. Ziel-SoC `charge_target_soc`), Ladeleistung ebenfalls über die laufende Ladephase gemittelt; beim Laden aus PV Plausibilitätsprüfung mit PV-Prognose (`forecast_entity`, Resttag heute in kWh) oder Sonnenuntergang – reicht die Sonne nicht, erscheint „heute ca. 85 %“; angezeigte Uhrzeiten ändern sich erst bei mehr als 20 min Abweichung, die 3 min anhält
- Ladezeit des Fahrzeugs an der Wallbox („80 % ca. 14:40“): Kapazität und Ladeziel fest oder aus Sensoren (`capacity_entity`, `target_entity`), Ladeleistung über die laufende Ladephase gemittelt; bei PV-Ladung Prüfung mit PV-Prognose minus Hausverbrauch (ohne Wallbox) bis Sonnenuntergang minus Bedarf des Hausakkus – reicht es nicht, erscheint „heute ca. 45 %“; optional Lademodus (`mode_entity`, z. B. EVCC off/now/minpv/pv; bei Min+PV Rest nach Sonnenuntergang mit `min_power_w`) und Vorrang des Hausakkus bis zu einem Ladestand (`priority_entity`, z. B. EVCC „Haus hat Priorität“); weitere optionale Ladesteuerungs-Sensoren: Dauerhaft laden (`always_entity`), Sonnenanteil (`solar_share_entity`), Mindeststrom und Phasen (`min_current_entity`, `phases_entity`), günstiges Netzladen (`grid_cost_entity`), Ladeplan (`plan_active_entity`, `plan_end_entity`)
- Autarkie als Tageswert (aus Netzbezug heute und Hausverbrauch heute oder eigenem Sensor), wahlweise live
- Wallbox wahlweise nur beim Laden, immer oder nie, mit Ladestand des Fahrzeugs
- Einklappbare Verbraucherliste in fester Reihenfolge, nur aktive Verbraucher, mit eigenem Bild oder Symbol
- Jedes Gerät merkt sich, ob die Verbraucherliste auf- oder zugeklappt ist (im Browser bzw. in der App gespeichert; abschaltbar). Karten mit gleichem Titel der Verbraucherliste teilen sich den Zustand, auch über Dashboards hinweg; für getrennte Zustände `storage_key: <beliebiger Name>` je Karte setzen
- Tippen, Halten und Doppeltippen mit den üblichen Home-Assistant-Aktionen
- Tempo der Linien zeigt die Leistung: Bezug ist die übliche Höchstleistung der letzten 12 Monate aus der HA-Langzeitstatistik (oder ein fester Wert)
- Mehrere Anlagen: weitere PV-Anlagen für Eigenverbrauch (summiert, mit Einzelwerten; eine davon optional als eigener Knoten oben rechts – mit Linie in die Haupt-PV oder in den Akku, z. B. für eine Garage-PV mit eigener Batterie), mehrere Akkus (Leistung summiert, Ladestand nach Kapazität gemittelt; ein Akku optional getrennt mit eigenem Knoten, z. B. Garage-PV → Garagen-Akku → Haus; Überschuss der Garage-PV fließt ins Haus bzw. Netz, kreuzende Linien werden als Brücke dargestellt; auch PV→Haus läuft als Brücke über die Netz-Akku-Linie) und Volleinspeise-Anlagen oben links mit eigener Linie direkt ins Netz – wahlweise als ein Knoten mit Summe oder ein Knoten je Anlage (max. 2)
- Netz zeigt den Hausanschluss, auf Wunsch zusätzlich die Volleinspeisung und die Summe aller Einspeisungen
- Symbolstil der Verbraucherliste separat wählbar; bei Linie oder HA-Symbol kompakt in drei Spalten; Spaltenzahl auch fest wählbar (2, 3 oder 4 nebeneinander, `consumers_columns`)
- Dezenter Link zum Energie-Dashboard (abschaltbar)
- Symbolstil wählbar: 3D (isometrisch), 2D (flach) oder Linie wie die HA-Icons, Symbole aus [smart-home-icons](https://github.com/LinnFidelius/smart-home-icons)
- Grafischer Editor, gegliedert nach Allgemein, PV, Netz, Akku, Haus, Wallbox und Verbrauchern


## Installation über den Marketplace

Ab Home Assistant 2026.11 (vorher HACS):

1. Einstellungen → Marketplace → „Über Link hinzufügen“
2. Repository: `https://github.com/LinnFidelius/energiefluss-card`, Typ: Dashboard
3. „Energiefluss Card“ installieren und die App neu laden
4. Karte hinzufügen → „Energiefluss“

Mit HACS vor 2026.11 genauso über „Benutzerdefinierte Repositories“.

## Bilder

Alle Symbole sind in die Karte eingebettet, es müssen keine Dateien kopiert werden. Im Editor lässt sich pro Knoten und Verbraucher ein eingebautes Symbol aus der Liste wählen oder ein eigener Pfad eintragen (z. B. `/local/meine-bilder/pv.png`).

In YAML steht `ef:<name>` für ein eingebautes Symbol: `pv`, `netz`, `akku`, `haus`, `wallbox`, `waschmaschine`, `waschmaschine-2`, `trockner`, `kuehlschrank`, `klima`, `tv`, `schreibtisch`, `schreibtisch-2`, `serverschrank`, `heisswasserhahn`, `sprudelhahn`, `zwischenstecker`, `waermepumpe`, `warmwasser`, `gas`, `wasser`, `balkonkraftwerk`, `e-auto`, `geschirrspueler`, `herd`, `mikrowelle`, `kaffeemaschine`, `heissluftfritteuse`, `desktop-pc`, `laptop`, `tablet`, `handy`, `router`, `access-point`, `saugroboter`, `ventilator`, `videoklingel`, `kamera`, `bewegungsmelder`, `temperatursensor`, `fensterkontakt`, `thermostatkopf`, `heizkoerper`, `relais`, `rollladen`, `plotter`, `gluehbirne`, `spot`, `tischleuchte`, `lichtleiste`, `garage`, `haustuer`, `terrasse`, `poolpumpe`, `wischroboter-station`, `rauchmelder`, `wassersensor`, `steckdosenleiste`, `smart-speaker`, `drucker`, `nas`, `switch`, `server`, `backup-server`. Weitere Symbole (Dienste, Apps, Essen, Getränke) gibt es im Repo [smart-home-icons](https://github.com/LinnFidelius/smart-home-icons).

## Updates

Neue Versionen erscheinen als GitHub-Release. Der Marketplace zeigt sie als Update an; nach dem Aktualisieren die App bzw. den Browser neu laden.

## Entwicklung

Die SVGs liegen im Ordner `icons`. Nach Änderungen dort `python3 tools/embed_icons.py` ausführen, das schreibt sie in den Block `EF_ICONS` der Karte.

## Beispiel-Konfiguration

```yaml
type: custom:energiefluss-card
pv:
  entity: sensor.pv_power
grid:
  entity: sensor.grid_power
battery:
  soc_entity: sensor.battery_soc
  charge_entity: sensor.battery_charge_power
  discharge_entity: sensor.battery_discharge_power
  capacity_kwh: 7.78
  min_soc: 6
home:
  entity: sensor.house_consumption
wallbox:
  entity: sensor.wallbox_power
  unit: kW
consumers:
  - entity: sensor.washing_machine_power
    name: Waschmaschine
    image: ef:waschmaschine
    threshold: 5
```

## Feedback

Wünsche und Fehler gerne über [Issues](../../issues/new/choose) melden (GitHub-Konto nötig). In der Energiefluss Card führt auch der Link unten im Karten-Editor dorthin.

## Hinweise

- Code, Symbole und Texte dieses Projekts wurden mit Claude (KI von Anthropic) erstellt und vom Betreiber des Repositorys geprüft und getestet.
- Privates Hobbyprojekt ohne Gewähr und ohne Support-Zusage. Nutzung auf eigene Verantwortung.
- Kein offizielles Home-Assistant-Projekt und mit keinem Gerätehersteller verbunden.
- Die Karte liest nur Sensorwerte aus Home Assistant und sendet keine Daten nach außen.

## Lizenz

MIT, siehe [LICENSE](LICENSE). Gilt für Code und Symbole.

## Mehrere Anlagen (Beispiel)

```yaml
type: custom:energiefluss-card
pv:
  entity: sensor.pv_dach_power
  name: Dach
  extra:
    - entity: sensor.pv_garage_power
      name: Garage
      secondary_entity: sensor.pv_garage_today
      node: battery   # eigener Knoten oben rechts; pv = Linie in die Haupt-PV, battery = Linie in den Akku
battery:
  soc_entity: sensor.akku1_soc
  charge_entity: sensor.akku1_charge
  discharge_entity: sensor.akku1_discharge
  extra:
    - name: Akku 2
      soc_entity: sensor.akku2_soc
      power_entity: sensor.akku2_power
      capacity_kwh: 10
      min_soc: 5
      separate: true   # eigener Knoten; die Garage-PV mit node: battery lädt dann nur diesen Akku
feed_in:
  layout: combined   # oder separate
  systems:
    - entity: sensor.anlage_sued_power
      name: Süd
      secondary_entity: sensor.anlage_sued_today
    - entity: sensor.anlage_west_power
      name: West
grid:
  entity: sensor.grid_power
  show_feed_in: true
  show_total: true
```

Der Netz-Sensor misst dabei nur den Hausanschluss; die Volleinspeise-Anlagen haben eigene Sensoren.
