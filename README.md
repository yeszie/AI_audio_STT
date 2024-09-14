# Transkrypcja i analiza plików audio z Whisper i GPT-4

Aplikacja oparta na Flasku umożliwia przesyłanie plików audio, które są następnie transkrybowane za pomocą modelu **Whisper** (API OpenAI), a przetranskrybowany tekst jest analizowany przez model **GPT-4**. Projekt oferuje wszechstronne narzędzie, które można rozbudować na wiele różnych sposobów, takich jak tłumaczenie, generowanie streszczeń czy analiza sentymentu.

## Główne funkcje aplikacji

1. **Interfejs HTML**:
   - Użytkownik przesyła plik audio (np. MP3, WAV, MP4) przez formularz na stronie.
   - Formularz przesyła plik na serwer, gdzie następuje jego przetwarzanie.

2. **Transkrypcja za pomocą Whisper**:
   - Skrypt korzysta z Whisper, który przekształca plik audio na tekst.
   - Whisper automatycznie wykrywa mowę oraz język nagrania (np. polski). Wynik transkrypcji jest przekazywany do GPT-4 do dalszej analizy.

3. **Analiza tekstu przez GPT-4**:
   - GPT-4 analizuje przetranskrybowany tekst i generuje odpowiedzi w zależności od ustawień. 
   - Użytkownik może kontrolować kreatywność odpowiedzi za pomocą parametru **temperatury**:
     - **Temperatura 0.0** – odpowiedzi są przewidywalne i bardziej konserwatywne.
     - **Temperatura 1.0** – odpowiedzi są bardziej losowe, kreatywne i mogą zawierać mniej oczywiste sugestie.

4. **Możliwość rozbudowy o funkcję monitorowania zużytych tokenów**:
   - Obecnie aplikacja nie wyświetla liczby zużytych tokenów, jednak możliwa jest rozbudowa skryptu, aby monitorować ilość zużytych tokenów, co pozwala kontrolować koszty użycia API.

## Przykłady zastosowań i pomysły na rozbudowę

### 1. **Tłumaczenie różnych języków**:
   Aplikacja może być rozbudowana o funkcję automatycznego tłumaczenia przetranskrybowanego tekstu z jednego języka na inny (np. z polskiego na angielski).

### 2. **Automatyczne streszczenie i podsumowanie**:
   GPT-4 może generować streszczenia długich nagrań, takich jak spotkania biznesowe, podcasty czy wykłady.

### 3. **Analiza i klasyfikacja sentymentu**:
   Możliwa jest rozbudowa o funkcję analizy sentymentu (pozytywny, neutralny, negatywny), co może być przydatne w analizie rozmów z klientami.

### 4. **Tworzenie transkrypcji dla celów edukacyjnych**:
   Aplikacja może automatycznie generować transkrypcje z lekcji, webinarów czy kursów online, co ułatwi przyswajanie treści.

### 5. **Generowanie treści na podstawie transkrypcji**:
   GPT-4 może przekształcić transkrypcje w artykuły, wpisy blogowe lub treści marketingowe.

### 6. **Automatyczna obsługa klienta (chatboty)**:
   Aplikacja może zostać zintegrowana z chatbotami, które przetwarzają wiadomości głosowe klientów i generują odpowiedzi.

### 7. **Transkrypcja wielojęzycznych nagrań**:
   Whisper automatycznie rozpoznaje język mowy, co jest przydatne w przypadku transkrypcji rozmów w różnych językach.

### 8. **Generowanie raportów z nagrań**:
   Aplikacja może automatycznie tworzyć raporty ze spotkań biznesowych czy sesji konsultacyjnych na podstawie transkrypcji.

## Klucz API i koszty

Do działania aplikacji wymagany jest **klucz API OpenAI**, który umożliwia komunikację z modelami Whisper i GPT-4. Należy pamiętać, że każde zapytanie do API zużywa tokeny, co generuje **koszty**. Koszty te zależą od liczby zużytych tokenów, dlatego zaleca się monitorowanie wykorzystania API, szczególnie przy intensywnym korzystaniu z aplikacji.

## Instalacja

1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/twojerepo.git
   cd twojerepo
