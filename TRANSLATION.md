# QTodoTxt translations

## Web translation:
You can help with translation, and without programming using a web service WebLate
https://hosted.weblate.org/projects/qtodotxt/

## For translation in your language is necessary:

1. The change in the script "pylupdate.py" variable "local"
2. Execute "pylupdate.py" with parameter "upd"
3. Open the file in the i18n directory with the name of the required translation
	- the file can be edited with a standard text editor and a specialized software package from QT - linguist
4. To eliminate the old translation execute "pylupdate.py" with parameter "clr"
5. After making changes, run the script "pylupdate.py" with the parameter "fix"
6. That's all


The program runs itself determines the translation used in accordance with the localization system in which it is running.

Variable "local" is a string of the form "language_country", where language is a lowercase, two-letter ISO 639 language code, and country is an uppercase, two- or three-letter ISO 3166 country code.
Example: "ru_RU", "de_DE", "fr_FR", "pl_PL"
