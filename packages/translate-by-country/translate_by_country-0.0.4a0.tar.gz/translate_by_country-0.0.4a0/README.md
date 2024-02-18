translate-by-country
====================

With this library, you can translate the text without choosing the language and with the characteristics of the countries

installation:
-------------

.. code-block:: text

    pip install translate-by-country

Usage:
------

Translates text based on country alpha2

.. code-block:: python

    from translate_by_country import translate_text_by_alpha2
    print(translate_text_by_alpha2("hello world","ax"))


Translates text based on country alpha3

.. code-block:: python

    from translate_by_country import translate_text_by_alpha3
    print(translate_text_by_alpha3("hello world","aut"))

Translates text based on country code

.. code-block:: python

    from translate_by_country import translate_text_by_code
    print(translate_text_by_code("hello world",98))

Translates text based on country name

.. code-block:: python

    from translate_by_country import translate_text_by_name
    print(translate_text_by_name("hello world","albania"))

Translates text based on country emoji

.. code-block:: python

    from translate_by_country import translate_text_by_name
    print(translate_text_by_emoji("hello world","🇹🇼"))
