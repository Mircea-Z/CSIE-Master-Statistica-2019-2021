# __Master Statistica 2019-2021__
Acesta este repository-ul promotiei 2019-2021 a masterului de statistica CSiE. Ne va fi util pentru a putea stoca proiecte si pentru a ne obisnui cu modul de lucru bazat pe version control.

## __Instructiuni de instalare/conectare__

* Pentru inceput veti avea nevoie de un cont gratuit GitHub. Il puteti crea urmand [acest](https://www.wikihow.com/Create-an-Account-on-GitHub) ghid. Contul va va permite sa primit acces de editare a acestui repo.
* Pentru a putea interactiona cu repository-ul va fi nevoie sa instalati local [GitBash](https://gitforwindows.org/) (Windows) sau puteti folosi un tool grafic cum ar fi [GitExtensions](http://gitextensions.github.io/).
Pentru cei cu MacOS exista o serie de clienti pe care ii puteti gasi [aici](https://git-scm.com/download/gui/mac) iar daca preferati linia de comanda puteti urma [acest](https://www.atlassian.com/git/tutorials/install-git) ghid.
* Pentru a aduce local fisierele si structura de foldere a repository-ului va trebui sa-l clonati. Gasiti [aici](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository) un ghid text.

## __Instructiuni de editare__

### Acces

* Accesul la repository-uri GitHub se poate face in doua feluri, fie printr-o combinatie user/parola fie prin SSH folosind o pereche de chei publica/privata. Acest acces va trebui acordat individual de catre cel care gestioneaza repo-ul. Asadar pentru acces va rog sa-mi scrieti un mesaj privat pe WhatsAPP cu user-ul vostru de GitHUB sau cu cheia __PUBLICA__ pe care doriti sa o adaug.

  - pentru a genera o pereche de chei SSH puteti folosi [acest](https://inchoo.net/dev-talk/how-to-generate-ssh-keys-for-git-authorization/) ghid.
  - pentru mai multe informatii despre SSH in general puteti vezita [resursa](https://www.ssh.com/ssh/key) oficiala

* Propun sa mentinem [ramura/branch-ul](https://guides.github.com/introduction/flow/) master gol (sau sa contina doar acest readme)

* Fiecare utilizator va avea un branch propriu pe care va avea acces de editarea protejat

### Mod de lucru

* Folosind GitBash sau linia de comanda preferata care suporta Git navigati pana la folderul in care doriti sa tineti fisierele din repo si introduceti comanda:

> git clone https://github.com/Mircea-Z/CSIE-Master-Statistica-2019-2021.git

ca in aceasta imagine:
![clone](clone.png)

Git va recrea automat structura de foldere din repository si va aduce ultima versiune a tuturor fisierelor.

* Folosind comanda "cd" navigati in folderul principal: ![cd](cd.png)

* Folosind comanda "git checkout" schimbati ramura la cea care va corespunde ![checkout](checkout.png)

* Dupa ce ne-am facut modificarile, adaugat fisierele si am terminat in general de lucrat local, si suntem gata de a publica ceea ce am facut folosim comanda "git status" pentru a vedea modificarile fata de versiunea curenta a ramurii: ![status](status.png)
* Folosind "git add" putem adauga in branch fisierele pe care le dorim. Parametrul ""--all" le adauga pe toate insa putem specifica de asemenea fisiere individuale cu "git add calea/catre/fisier.fis": ![staging](staging.png)
Vedem atunci in "status" ca toate fisierele sunt acum trecute cu verde.
