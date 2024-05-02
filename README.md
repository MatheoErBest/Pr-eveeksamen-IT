# Oversikt
I dette prosjektet har jeg lagd en app som har et simpelt spill med en meny og en innloggings side. Med innloggingen må man først registrere en bruker og så kan man logge inn. Passord og brukernavn blir lagret i en database som er kryptert fordi det er passord inni kolonnene.

# Feilsøking
Gjennom prosjektet her har jeg støtt på mange problemer, mest når det kom til å koble databasen sammen med koden, og sende info til databasen siden den ville ikke ta imot tekst. For å fikse dette brukte jeg mye forum og openAI. Noe greide jeg å fikse selv, men det var ikke alt jeg fikk fikset, som da databasen ikke tok imot tekst. Det var et annet problem med at brukeren 'matheo' ville ikke kobles til, dette fikset jeg ved å sette et nytt passord og når jeg dobbelsjekket brukerene på serveren hadde jeg også skrivd brukernavnet mitt feil.

# Brukertesting Spørsmål
1. Er det lett å skjønne hvordan man logger inn?
2. Uten innstruksjoner hvor langt tror du man kunne ha kommet i programmet før man kommer til en full stans.
3. Er det noen endringer du ville gjort?
4. Var det noe annet du ville lagt til?
5. Noe ekstra tibakemeldinger?


# Hvordan bruke appen
1. Logge inn:
For å logge inn mp du starte med  skrive inn et brukernavn og passord, så trykker du registrer så logg in.

2. Starte et spill
Å starte et spill er ganske lett, det er bare å navigere med piltastene dine til 'Start Game' så trykker du enter.

3. Hvordan funker spillet?
Spillet fungererved å bevege karakteren din med w a s d og man bytter rom med spacebar. Målet er å finne den blåe firkanten. ESC går ut av spillet og lagrer scoren din i en database med et brukernavn.