# Attack on SCADA system

Ovaj projekat je usmeren na bezbednost SCADA sistema i simulira okruženje nuklearnog postrojenja. Projekat je organizovan u četiri glavna foldera:

## 1. Materijali

Folder `Materijali` sadrži sve materijale korišćene tokom razvoja projekta. To uključuje istraživačke radove i druge relevantne resurse za projekat.

## 2. SCADA HMI

U folderu `SCADA HMI` smeštena je aplikacija (HMI) odgovorna za prikaz podataka dobijenih od simuliranog postrojenja. Dodatno, sadrži model za predviđanje potencijalnih napada. HMI aplikacija predstavlja centralni interfejs za kontrolu i praćenje simuliranog nuklearnog postrojenja.

## 3. Simulator Postrojenja

U folderu `Simulator Postrojenja` nalazi se simulator nuklearnog postrojenja. Ovaj deo emulira deo nuklearnog postrojenja i komunicira sa SCADA HMI aplikacijom. Simulator generiše podatke, simulirajući scenarije iz stvarnog sveta koje HMI prati i kontroliše.

## 4. Man-in-the-Middle

Folder `Man in the middle` sadrži aplikaciju dizajniranu za izvođenje napada na sistem.

