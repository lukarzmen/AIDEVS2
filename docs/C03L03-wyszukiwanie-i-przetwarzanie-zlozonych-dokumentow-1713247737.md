![](https://assets.circle.so/pubdxqnwjw9ewyrhj9o5csbb91lk)

» [Lekka wersja przeglądarkowa](https://cloud.overment.com/C03L03-wyszukiwanie-1712221062.html) «

Długoterminowa pamięć dla modelu jest jednym z najbardziej użytecznych zastosowań LLM, jakie znam. Pierwszym powodem jest możliwość **hiperpersonalizacji** doświadczeń (to moje określenie dla połączenia wiedzy na nasz temat z dostępem do usług i urządzeń). Natomiast drugi powód dotyczy **możliwości zbudowania częściowo autonomicznych zachowań**, co także przekłada się na niespotykane wcześniej zastosowania. Dość łatwo można sobie to wyobrazić, poprzez wyobrażenie prostego zadania, które GPT-4 wykonuje samodzielnie, posiadając zdolność dobierania niezbędnych danych do jego wykonania. Oczywiście w tym momencie szczególną rolę odgrywa cytat z początku AI\_Devs: "GPT-4 potrafi więcej, niż myślimy i mniej niż nam się wydaje". Zobaczmy więc, co to dokładnie oznacza w praktyce.

## Czym są bazy wektorowe?

W lekcji **C01L02** poruszaliśmy temat tokenizacji oraz embeddingu. Bazy wektorowe pozwalają nam je przechowywać oraz przeszukiwać. Poniżej znajduje się **uproszczona wizualizacja** wielowymiarowych danych, przedstawionych w przestrzeni 3D. Możesz ją zobaczyć [tutaj](https://projector.tensorflow.org/).

![](https://assets.circle.so/uv71d2kugdbsqqsbirt9dzjx7xqe)

Dzięki technikom porównywania wektorów możliwe jest określenie **podobieństwa** pomiędzy nimi i tym samym odnalezienie zbliżonych danych. Przykładowo wykorzystując metodę **cosine similarity** otrzymujemy wartość od -1 do 1. (-1: semantycznie odwrotne, 0: semantycznie niepowiązane, 1: semantycznie powiązane). Za samo przeprowadzenie obliczeń mogą również odpowiadać bazy wektorowe, zwracając nam wyniki z "similarity score". Na podstawie tego wyniku możemy wybrać tylko te wpisy, które są najbardziej zbliżone znaczeniem do zapytania. Widać to obrazku poniżej, na którym słowo **komputer** zostało powiązane ze **sprzęt, oprogramowanie, programowanie, pc, grafika, IBM czy Macintosh**.

![](https://assets.circle.so/2geha7rx3aqku7lgyboyz3b7gpxk)

  
Możliwość odnajdywania treści **(nie tylko tekstu)** o podobnym znaczeniu, stanowi istotny **element** budowania dynamicznego kontekstu dla LLM. Co więcej, już teraz praca z bazami danych na podstawowym poziomie, może sprowadzać się do **prostej interakcji przez API** i zapytań CRUD. Nie oznacza to jednak budowanie dynamicznego kontekstu na potrzeby LLM, jest równie proste.

Poniższy schemat przedstawia proces dodawania danych do indeksu bazy wektorowej. Mówimy tutaj o:

1.  Przygotowaniu **dokumentu** w postaci **treści oraz metadanych**
    
2.  Wygenerowaniu embeddingu z pomocą np. text-embedding-3-large
    
3.  Zapisania embeddingu w bazie **w połączeniu z metadanymi**
    

  

![](https://assets.circle.so/qzdc9nz3j5dqhivyisvdf8c593gc)

W indeksowaniu danych istotną rolę odgrywają metadane, ponieważ embedding sam w sobie jest nieczytelny dla człowieka (jest to po prostu długa lista liczb, tzw. wektorów). W metadanych możemy zapisać:

*   Identyfikator (ID lub UUID) wpisu, który oryginalnie przechowywany jest w klasycznej bazie
    
*   Faktyczną treść dokumentu (chociaż zwykle polecam przechowywanie jej w klasycznej bazie, do której mamy bardzo łatwy dostęp z poziomu kodu)
    
*   Informacje opisujące dokument: np. kategorie, tagi, źródło lub inne dane, które mogą być istotne w kontekście **filtrowania, segmentowania czy łączenia ze sobą wielu części dłuższych dokumentów**
    

Dodatkowym aspektem wpływającym na złożoność indeksowania danych na potrzeby LLM jest fakt, że będziemy **dzielić dłuższe treści na mniejsze fragmenty (eng. chunk)**. Poza tym jest niemal pewne, że przynajmniej **część z indeksowanych danych będzie zmieniać się w czasie**. W związku z tym, że generowanie embeddingów kosztuje i/lub zajmuje czas, musimy zadbać o możliwość **synchronizacji** pomiędzy źródłem danych (czy to bazą SQL/noSQL), a indeksem bazy wektorowej.

## Similarity Search

Wyszukiwanie (tzw. Similarity Search) z pomocą baz wektorowych prezentuje poniższy schemat, który na pierwszy rzut oka wygląda podobnie jak samo indeksowanie, lecz różni się rodzajem operacji oraz danymi, które otrzymujemy. Konkretnie:

1.  Zapytanie może zostać wykorzystane bezpośrednio lub może być **wzbogacone, zmodyfikowane czy też opisane** w taki sposób, aby **zwiększyć szansę odnalezienia podobnych danych** lub **aby móc ograniczać zakres poszukiwania** lub **filtrować wyniki**.
    
2.  Embedding odbywa się na dokładnie takiej samej zasadzie jak wcześniej.
    
3.  W odpowiedzi otrzymujemy **listę embeddingów** oraz (zwykle) przypisany do nich **score** reprezentujący to **jak bardzo semantycznie zbliżone są do przesłanego zapytania**. Inaczej mówiąc: jak bardzo są do siebie podobne.
    

  

![](https://assets.circle.so/z4hs99rxgc06atcdxs4r6f42xzak)

W przykładzie [**21\_similarity**](https://github.com/i-am-alice/2nd-devs/tree/main/21_similarity) znajdziesz kod, którego zadaniem jest zbudowanie dynamicznego kontekstu **w zależności od tego, co wpisał użytkownik**. Konkretnie realizujemy w nim dokładnie te schematy, które omawiałem przed chwilą, czyli:

1.  Wczytuję treść pliku
    
2.  Dzielę ją na mniejsze fragmenty
    
3.  Tworzę store lub wczytuję go z pliku
    
4.  Wyszukuję podobne dokumenty na podstawie zapytania
    
5.  Buduję kontekst i pytam model
    

W punkcie 3. wykorzystuję **HNSWLib** jako in-memory vector store, który mogę zapisać w pliku, dzięki czemu **nie mam potrzeby przeprowadzania embeddingu dokumentów za każdym razem**.

> Info: Schemat działania bezpośrednio z bazami wektorowymi wygląda podobnie, o czym przekonamy się w dalszych lekcjach. Omówimy tam także podejście no-code do pracy z bazami wektorowymi.

![](https://assets.circle.so/kbdesjjgp5cejl0s26czjm1y4eup)

Jeśli chcesz, wróć teraz do przykładu **11\_docs** w którym pokazywałem jak generować dokumenty i opisywać je z pomocą metadanych. Dzięki temu łatwiej skojarzysz, dlaczego opisywanie danych jest tak istotne.

Konkretnie w kodzie powyżej w linii :7 korzystam z metody **similaritySearchWithScore** i jako drugi argument przekazuję wartość określającą to, **ile rekordów chcę otrzymać (tzw. topK)**. Zwiększenie tej wartości spowoduje zwrócenie większej liczby rekordów, które dodatkowo będziemy mogli przefiltrować lub pogrupować posługując się np. ich metadanymi. Samo filtrowanie może odbyć się także **już na etapie wyszukiwania**, ponieważ praktycznie każda baza wektorowa daje nam możliwość przekazania **obiektu** określającego **dopasowania metadanych**, które chcemy brać pod uwagę.

## Wyszukiwanie hybrydowe

Similarity Search i bazy wektorowe **nie są odpowiedzią na wszystkie pytania**. Początkowo robią świetne wrażenie i sprawdzają się na etapie prototypu. Jednak gdy zależy nam na budowaniu czegoś więcej niż interesujące demo, potrzebujemy czegoś więcej.

Wyszukiwanie nie jest nowym tematem w programowaniu. Co więcej, same bazy wektorowe również, ale teraz zwracają na siebie szczególną uwagę ze względu na popularyzację modeli językowych oraz ogólny rozwój technologii. Jak za chwilę się przekonamy, najlepsze rezultaty w pracy z własnymi danymi i dynamicznym kontekstem można uzyskać, **łącząc różne techniki wyszukiwania w tzw. Hybrid Search**, czyli wyszukiwanie hybrydowe. Obecnie takie połączenie na potrzeby LLM doczekało się nawet nazwy: HSRAG, czyli **Hybrid Search and Retrieval Augmented Generation**.

Zobaczmy jednak, na czym polega problem. Otóż powiedzieliśmy już, że w przypadku dłuższych treści, ze względu na limity kontekstu oraz optymalizację kosztów, musimy dzielić je na mniejsze fragmenty. Strategia podziału będzie różnić się na w zależności od struktury danych z którą pracujemy oraz tego, jaki rodzaj aplikacji budujemy.

Zakładając jednak najprostszy scenariusz, który polega na **możliwości rozmowy z własną bazą wiedzy**, musimy faktycznie wygenerować małe dokumenty. Ich długość powinna być wystarczająca, **aby zawierały informacje istotne dla modelu, możliwie bez zaburzania ich kontekstu**. Inaczej mówiąc, chcemy mieć fragmenty jak najkrótsze, ale też nie chcemy, aby stały się niezrozumiałe.

Spójrzmy na poniższy przykład pokazujący małą bazę wiedzy. Wyobraźmy sobie, że jest to długi dokument zawierający informacje na mój temat. Jeśli skorzystalibyśmy z bazy wektorowej do wyszukania fragmentów **powiązanych semantycznie z zapytaniem: "Czym zajmuje się Adam?"**, to dokument pierwszy oraz trzeci zostałby odnaleziony.

![](https://assets.circle.so/vsakzev9q3zrhpsbmkhizl1fw6cs)

O tym, że tak się stanie, możesz przekonać się w przykładzie [**22\_simple**](https://github.com/i-am-alice/2nd-devs/blob/main/22_simple/22.ts) w którym umieściłem trzy dokumenty. Następnie wykorzystuję prosty vector store, przechowujący je w pamięci i umożliwiający mi ich wyszukanie poprzez similarity search.

> Ważne! Pomimo tego, że modele do embeddingów od OpenAI potrafią pracować z językiem polskim, warto unikać mieszania języków. Oznacza to, że jeżeli bazę wiedzy budujesz po angielsku, to stosuj ten język także w przypadku kierowanej do niej zapytań

![](https://assets.circle.so/0jnt3nolw3ewp8q2apr17esczcp4)

Wyobraźmy sobie jednak nieco inny przypadek, który jest **niezwykle często spotykany w praktyce**. Chodzi o scenariusz w którym **interesująca nas informacja została rozbita na więcej niż jeden fragment**. Na obrazku poniżej widzimy, że opis mojej specjalizacji znajduje się w pierwszym, drugim i czwartym dokumencie. Niestety informacja z pierwszego fragmentu jest kontynuowana w drugim, który tym razem nie został wskazany jako istotny.

![](https://assets.circle.so/36altnnkf6xja2tk5z2lezrf2oyh)

Ponownie możemy się o tym przekonać w przykładzie [**23\_fragmented**](https://github.com/i-am-alice/2nd-devs/blob/main/23_fragmented/23.ts). Pomimo tego, że zwiększyłem limit wyszukiwania dokumentów (topK) na trzy pierwsze wyniki, to niestety nie ma wśród nich drugiego dokumentu. Oznacza to, że jeśli zbuduję teraz kontekst dla modelu, to udzielone przez niego odpowiedzi będą **niepełne**. I choć w tej sytuacji może bylibyśmy w stanie to wybaczyć, to w praktyce utrata precyzji jest bardzo niepożądana. Tym bardziej że niedokładne odnalezienie danych może zakończyć się wstrzyknięciem do kontekstu informacji, które doprowadzą do halucynacji modelu, czyniąc nasz system, bezużytecznym lub nawet szkodliwym.

![](https://assets.circle.so/ujolvyn4vxazm4f16ma7yc9w15f1)

O tym, jak sobie radzić w takich sytuacjach powiemy w kolejnych lekcjach, bo to trochę dłuższy temat i musimy poświęcić mu nieco więcej czasu.

## Praca z różnymi formatami plików

W lekcji **C01L05** mówiłem o organizacji oraz dostosowaniu danych. Przeniesiemy to teraz na nieco bardziej dosłowny wymiar.

Powszechnie wiadomo, że praca z różnymi formatami nieustrukturyzowanych danych jest wymagająca. W związku z tym, że jest to tak obszerne zagadnienie, przejdziemy sobie przez bardzo podobny przykład, jak [**12\_web**](https://github.com/i-am-alice/2nd-devs/blob/main/12_web/12.ts), jednak wykorzystamy wiedzę, którą zdobyliśmy od tamtej pory. Omawiany teraz kod znajdziesz w przykładzie [**24\_files**](https://github.com/i-am-alice/2nd-devs/blob/main/24_files/24.ts). I chociaż praca z różnymi formatami plików będzie się od siebie różnić, nasza uwaga będzie skupiona na możliwie uniwersalnych koncepcjach.

Naszym celem będzie zbudowanie zestawu danych, na podstawie informacji o nas, czyli twórcach AI\_Devs, bezpośrednio ze strony [aidevs.pl](http://aidevs.pl/). Dla ułatwienia, na początek zapiszę jej treść jako zwykły plik HTML, który wczytamy do kodu.

![](https://assets.circle.so/30qo8r7778jfflujcrtgv9om1qtv)

Oryginalny plik HTML co prawda mógłby zostać zrozumiany przez model, jednak mamy tutaj mnóstwo szumu w postaci tagów HTML, stylów CSS czy skryptów JavaScript. Podobnie wyglądałoby to także w przypadku innych formatów plików, może z wyłączeniem formatów typu .txt czy plików markdown.

![](https://assets.circle.so/g792m8v0xmmpmqig40e1l7prbey6)

Strona [aidevs.pl](http://aidevs.pl/) jest dość obszerna, a nam zależy tylko na jednej sekcji. Dobrym pomysłem będzie usunięcie całej reszty. W związku z tym, że mamy do czynienia z kodem HTML, możemy wykorzystać np. [cheerio](https://www.npmjs.com/package/cheerio) do pobrania treści wskazanego tagu. W naszym przypadku będzie to element div z identyfikatorem **instructors** (odnalazłem go w źródle strony korzystając z Chrome Dev Tools).

![](https://assets.circle.so/ekkb3xdo08byc6hboy2wvg9hcrqc)

Nasze dane dalej zawierają mnóstwo zbędnych elementów i warto byłoby zamienić ten kod na zwykły tekst, jednak trzeba wziąć pod uwagę jego docelowe zastosowanie, czyli wykorzystanie na potrzeby kontekstu dla LLM. Oznacza to, że nie zależy nam wyłącznie na tekście, ale także zachowaniu formatowania czy możliwości wyświetlania linków i obrazów. W przypadku większych źródeł danych istotne byłoby także podawanie źródeł jako referencji.

Najprostszym sposobem, jaki znam na przekonwertowanie HTML na użyteczny dla modelu tekst, jest zamiana go na składnię Markdown i możemy w tym celu wykorzystać gotowe narzędzia, np. [node-html-markdown](https://www.npmjs.com/package/node-html-markdown). Rezultat widać poniżej.

![](https://assets.circle.so/ks7mll0r97n0qthynlgmx6whr3zc)

Formą, do której dążymy, są dokumenty opisane metadanymi. Musimy więc podzielić ten tekst na mniejsze fragmenty. W związku z tym, że chodzi nam o uzyskanie informacji o trzech autorach, to zasadne wydaje się podzielenie treści na fragmenty opisujące każdego z nas.

Gdy spojrzymy na treść markdown, zobaczymy, że nagłówkami H3 (w markdown wyświetlanymi jako "###") możemy odróżnić poszczególne sekcje. Niestety nagłówki w strukturze HTML znajdują się **poniżej zdjęć**, więc je także musimy uwzględnić. Jeśli podzielimy tekst według znaków "###" to otrzymamy **błędny podział, widoczny po lewej**. Wówczas link do mojego zdjęcia znajdzie się poza dokumentem, który mnie opisuje, zdjęcie Kuby znajdzie się w moim dokumencie itd. Nas natomiast interesuje podział widoczny po prawej stronie.

![](https://assets.circle.so/ls5o0jxfuk8dgsxqmrgem6gs27mc)

Aby go osiągnąć, musimy skorzystać z wyrażenia regularnego. I tutaj **bardzo pomocna jest wiedza na ich temat**, jednak do napisania wyrażenia możemy wykorzystać GPT-4 i dokładnie to zrobiłem. Opisałem problem związany z podziałem i zapytałem o wyrażenie regularne, które go rozwiąże.

Mając odpowiednio podzielone treści, mogłem je opisać z pomocą metadanych. Tutaj również wykorzystałem wyrażenia regularne pobierające imiona autorów oraz dodałem dwie właściwości wpisane ręcznie (bo nie zawsze muszą być one generowane dynamicznie). Mając tak opisane dokumenty, jesteśmy już prawie gotowi, aczkolwiek wyraźnie widać, że znajdujące się w treści linki będą nam niepotrzebnie zużywać tokeny, więc musimy je przenieść do metadanych.

![](https://assets.circle.so/vuifkbkvuw941g42jw2uvp513hs1)

Tutaj ponownie skorzystałem z wyrażeń regularnych, aby odnaleźć linki znajdujące się w treści dokumentu. Następnie przeniosłem ich adresy do metadanych, a w treści wstawiłem odpowiadające im indeksy poprzedzone dolarem. W razie potrzeby można rozważyć inne oznaczenie, aby na późniejszym etapie móc wygodnie je podmienić w wypowiedzi modelu.

![](https://assets.circle.so/mpw3cv5u4yyg9tq3brtnq7b8tchn)

Tak przygotowane dokumenty są gotowe do indeksowania w bazie wektorowej oraz późniejszego wykorzystania na potrzeby dynamicznego kontekstu. Różnica pomiędzy oryginalnymi danymi a tymi powyżej, jest ogromna, co z pewnością będzie miało wpływ na efektywność naszego systemu. Jeśli chcesz, możesz wykorzystać wiedzę, którą już posiadasz, aby zbudować prostego czatbota, odpowiadającego na pytania na temat twórców AI\_Devs.

## Przetwarzanie długich dokumentów

Gdy będziesz pracować z danymi podłączanymi do LLM, to zwykle potrzebnych informacji będzie więcej, niż możemy zmieścić w kontekście. Mowa tutaj przynajmniej o kilku przypadkach:

*   **Przetworzeniu** całej treści długiego dokumentu, np. na potrzeby korekty czy tłumaczenia
    
*   **Klasyfikacji** dużych zestawów danych, np. z pomocą tagów, kategorii czy etykiet
    
*   **Wzbogacaniu** danych na potrzeby użytkownika bądź systemu (np. wyszukiwania czy rekomendacji)
    
*   **Kompresji** obszernych treści, np. poprzez podsumowanie, co może być przydatne nie tylko na potrzeby użytkownika, ale także samego systemu. Niekiedy chcąc indeksować duże bazy danych, będzie nam zależało na wygenerowaniu podsumowań istotnych dla nas zagadnień
    
*   **Interakcji** z danymi w postaci czatbota lub w celu sięgania po zewnętrzne informacje na potrzeby realizowanego zadania
    

Aby zobrazować Ci, o co tutaj chodzi, tym razem wykorzystamy platformę [make.com](http://make.com/) do przygotowania prostego scenariusza. Możesz wykorzystać go w połączeniu ze swoim kodem lub wprost odwzorować jego mechanikę z pomocą kodu.

![](https://assets.circle.so/5bg4ao4yh2yx2pirbor1mze43yw5)

> UWAGA: Do testów tego scenariusza wykorzystaj krótkie pliki. W związku z tym, że działa z modelem GPT-4, należy mieć na uwadze koszty przetwarzania długich treści

*   ⚡ [Pobierz Blueprint Scenariusza](https://cloud.overment.com/aidevs_process_file-1695994995.json)
    

Przyjrzyjmy się temu bliżej:

*   Scenariusz rozpoczyna się webhookiem na który możemy przesyłać pliki z pomocą zapytań HTTP z naszej aplikacji lub innych scenariuszy Make
    
*   Treść pliku jest zapisywana w zmiennej oraz **dzielona na mniejsze fragmenty** na podstawie **znaku podwójnej nowej linii**
    
*   Poszczególne fragmenty trafiają do OpenAI w połączeniu z instrukcją **przetłumaczenia** ich na język angielski
    
*   W sytuacji, gdy z jakiegoś powodu OpenAI nie odpowie, podejmujemy próbę naprawienia błędu poprzez **poczekanie oraz wznowienie akcji**
    
*   Po przetworzeniu fragmentów zapisujemy ich treść na Google Drive i generujemy link do pobrania
    
*   Link do pliku przesyłamy w odpowiedzi
    

Zanim przejdziemy dalej, chciałbym zwrócić Twoją uwagę na kilka rzeczy:

*   Powyższy scenariusz realizuje **izolowane zadanie** i może zostać wywołany na różne sposoby. Może się to odbywać na żądanie (np. w trakcie rozmowy z AI), według harmonogramu (np. o ustalonej porze) lub w wyniku jakiegoś zdarzenia (np. dodania pliku do Google Drive). Czyni to go bardzo elastycznym i według mojego doświadczenia, znacznie podnosi jego użyteczność
    
*   Poza samym plikiem można przekazać dodatkowe informacje **nadające kontekst** lub w ogóle modyfikujące instrukcję systemową. Wówczas użyteczność rozwiązania rośnie jeszcze bardziej
    
*   Scenariusz o praktycznie dokładnie takiej samej strukturze wykorzystywałem już wielokrotnie na potrzeby tłumaczeń treści o długości ~25 000 znaków. W przypadku dłuższych form (np. książek), **należy rozważyć przełożenie tej logiki na kod**, ze względu na znacznie większą kontrolę nad ewentualnymi błędami oraz czystą oszczędnością wynikającą z liczby wykonanych operacji za które rozlicza nas [make.com](http://make.com/)
    

W związku z tym, że przetwarzanie pliku odbywa się automatycznie, musimy zadbać o to, aby model brał pod uwagę fakt, że ma do czynienia z **fragmentami** dłuższego dokumentu. Ze względu na bardzo prostą logiką podziału treści, może zdarzyć się tak, że fragmentem będzie np. jedno zdanie. Warto więc nadać **dodatkowy kontekst** poprzez przekazanie nazwy pliku lub innych pomocnych informacji, które pozwolą lepiej dopasować tłumaczenie, szczególnie w przypadku słów i wyrażeń posiadających różne znaczenia.

  

![](https://assets.circle.so/vj9bxnteyj6le35wmkxjbwz9gi9e)

  

Samo działanie scenariusza można przetestować z pomocą poniższego CURL'a lub zapytania HTTP w dowolnej innej formie. Oczywiście należy podmienić nazwę pliku oraz adres webhooka powiązanego ze scenariuszem.

![](https://assets.circle.so/hgjznu6n6uwonaxgcxt2oa68aqwz)

  
Scenariusz przetwarzający pliki można także uruchamiać innym. Przykładowo możesz utworzyć **inny katalog na Google Drive, np. "Do przetłumaczenia"** i "obserwować" go z pomocą scenariusza [make.com](http://make.com/) lub uruchamiać np. raz dziennie. Jest to przykład tego, o czym wspominałem wcześniej, czyli korzyści wynikających z "izolowania" scenariuszy realizujących konkretne zadania.

![](https://assets.circle.so/83vy8y4e9coomyivn2voxq3jxbsc)

*   ⚡ [Pobierz blueprint](https://cloud.overment.com/aidevs_watch_folder-1695994706.json)
    

Poza podłączeniem konta Google oraz wskazaniem katalogów na których automatyzacja ma pracować, w module "Process" należy podmienić adres Webhooka na ten, kierujący do automatyzacji odpowiedzialnej za faktyczne tłumaczenie. W związku z tym, że scenariusz "Watch Files" rozpoczyna się wyzwalaczem (triggerem) typu "Acid", jego reakcja nie będzie natychmiastowa. Obecność nowych plików będzie sprawdzana według ustalonego harmonogramu (dostępnego w ustawieniach automatyzacji, w lewym, dolnym rogu ekranu).

* * *

## Zadanie praktyczne

> Dzisiaj tylko jedno zadanie praktyczne, ponieważ jest nieco bardziej skomplikowane niż dotychczasowe. Powodzenia!

  

*   Rozwiąż zadanie o nazwie “**whoami**”. Za każdym razem, gdy pobierzesz zadanie, system zwróci Ci jedną ciekawostkę na temat pewnej osoby. Twoim zadaniem jest zbudowanie mechanizmu, który odgadnie, co to za osoba. W zadaniu chodzi o utrzymanie wątku w konwersacji z backendem. Jest to dodatkowo utrudnione przez fakt, że token ważny jest tylko 2 sekundy (trzeba go cyklicznie odświeżać!). Celem zadania jest napisania mechanizmu, który odpowiada, czy na podstawie otrzymanych hintów jest w stanie powiedzieć, czy wie, kim jest tajemnicza postać. Jeśli odpowiedź brzmi NIE, to pobierasz kolejną wskazówkę i doklejasz ją do bieżącego wątku. Jeśli odpowiedź brzmi TAK, to zgłaszasz ją do /answer/. Wybraliśmy dość ‘ikoniczną’ postać, więc model powinien zgadnąć, o kogo chodzi, po maksymalnie 5-6 podpowiedziach. Zaprogramuj mechanizm tak, aby wysyłał dane do /answer/ tylko, gdy jest absolutnie pewny swojej odpowiedzi.
    

* * *

## Sprawdź swoją wiedzę

[Rozpocznij Quiz](https://tasks.aidevs.pl/quiz/c03l03_rtta)

* * *

## Podsumowanie Audio