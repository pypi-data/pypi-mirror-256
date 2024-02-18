# translate-by-country

With this library, you can translate the text without choosing the language and with the characteristics of the countries
<hr>

# installation:

```
pip install translate-by-country
```
<hr>

# Usage:
<br>

Translates text based on country alpha2
```
from translate_by_country import translate_text_by_alpha2

print(translate_text_by_alpha2("hello world","ax"))
```
<br>
Translates text based on country alpha3

```
from translate_by_country import translate_text_by_alpha3

print(translate_text_by_alpha3("hello world","aut"))
```

<br>
Translates text based on country code

```
from translate_by_country import translate_text_by_code

print(translate_text_by_code("hello world",98))
```
<br>
Translates text based on country name

```
from translate_by_country import translate_text_by_name

print(translate_text_by_name("hello world","albania"))
```