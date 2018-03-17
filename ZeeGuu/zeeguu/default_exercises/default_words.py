# This Python file uses the following encoding: utf-8

"""
    When a new anonymous, or even not anonymous user
    is created, it's good to already offer them some
    words to be able to practice.

    This file takes care of this for the moment.

"""
import zeeguu
from zeeguu.model import Bookmark

bookmark_data = dict()

lingnaut_nl = 'http://www.linguanaut.com/english_dutch.htm'
bookmark_data['nl'] = [
    ["voorsichtig", "careful", "Wees voorsichtig!", lingnaut_nl],
    ["waar", "where", "Waar woont u?", lingnaut_nl],
    ["begrijp", "understand", "Ik begrijp het niet", lingnaut_nl],
    ["geweldig", "great", "Dat is geweldig!", lingnaut_nl],
    ["zeg", "say", "Hoe zeg je “Please” in het Nederlands?", lingnaut_nl],
    ["slecht", "bad", "Mijn Nederlands is slecht.", lingnaut_nl],
    ["oefenen", "practice", "Ik moet mijn Nederlands oefenen.", lingnaut_nl],
    ["zorgen", "worry", "Maak je geen zorgen", lingnaut_nl],
    ["Haast", "Hurry", "Haast je!", lingnaut_nl],
    ["nodig", "needed", "Ik heb een dokter nodig.", lingnaut_nl],
    ["terug", "back", "Ik ben zo terug.", lingnaut_nl],
    ["hou van", "like", "Ik hou van de Nederlandse taal", lingnaut_nl]
]

lingnaut_de = 'http://www.linguanaut.com/english_german.htm'
bookmark_data['de'] = [
    ["Ahnung", "idea", "Ich habe keine Ahnung.", lingnaut_de],
    ["jederzeit", "anytime", "Du kannst mich jederzeit anrufen", lingnaut_de],
    ["fällig", "due", "	Die Telefonrechnung ist fällig", lingnaut_de],
    ["vermisse", "miss", "	Ich vermisse dich", lingnaut_de],
    ["einladen", "invite", "Ich möchte Dich zum Abendessen einladen.", lingnaut_de],
    ["esse", "eat", "	Ich esse kein Schweinefleisch!", lingnaut_de],
    ["gehen", "to go", "Möchtest Du spazieren gehen?", lingnaut_de],
    ["verheiratet", "married", "Ich bin verheiratet", lingnaut_de],
    ["schön", "beautiful", "Du siehst schön aus!", lingnaut_de],
    ["Abendessen", "dinner", "Ich möchte Dich zum Abendessen einladen.", lingnaut_de],
    ["langweilig", "boring", "Mir ist langweilig", lingnaut_de]
]

lingnaut_es = 'http://www.linguanaut.com/english_spanish.htm'
bookmark_data['es'] = [
    ["Dónde", "where", "¿Dónde Vives?", lingnaut_es],
    ["Sueños", "dreams", "¡Buenas Noches Y Dulces Sueños!", lingnaut_es],
    ["País", "country", "Me Gustaría Visitar Algún Día Tu País", lingnaut_es],
    ["Gustaría", "I'd like to", "Me Gustaría Visitar Algún Día Tu País", lingnaut_es],
    ["Saludos", "greetings", "Dale Saludos A Juan De Mi Parte", lingnaut_es],
    ["Despacio", "slow", "¡Puedes Hablar Más Despacio!", lingnaut_es],
    ["Entiendo", "understand", "¡No Entiendo!", lingnaut_es],
    ["Malo", "bad", "Mi Español Es Malo", lingnaut_es],
    ["Hambre", "hunger", "Tengo Hambre", lingnaut_es],
    ["Mareado", "sick", "Estoy Mareado.", lingnaut_es],
    ["tomar", "drink", "Qué le gustaría tomar?", lingnaut_es]
]

lingnaut_fr = 'http://www.linguanaut.com/english_french.htm'
bookmark_data['fr'] = [
    ["perdu", "lost", "Je suis perdu", lingnaut_fr],
    ["toilettes", "toilet", "	Où sont les toilettes?", lingnaut_fr],
    ["Allez", "go", "Allez tout droit!", lingnaut_fr],
    ["cherche", "looking for", "Je cherche Jean", lingnaut_fr],
    ["Combien", "how much", "Combien cela coûte?", lingnaut_fr],
    ["Viens", "come", "Viens avec moi!", lingnaut_fr],
    ["Où", "where", "Où vis-tu?", lingnaut_fr],
    ["merveilleux", "wonderful", "La France est un pays merveilleux", lingnaut_fr],
    ["Il faut que je", "I have to", "Il faut que je parte.", lingnaut_fr],
    ["nuit", "night", "Bonne nuit et fais de beaux rêves!", lingnaut_fr],
    ["rêves", "dreams", "Bonne nuit et fais de beaux rêves!", lingnaut_fr]
]


def create_default_bookmarks(session, user, language_code):
    bookmarks = []

    try:

        print("trying to load default bookmarks for " + str(user.name))
        for data_point in bookmark_data[language_code]:
            bookmark = Bookmark.find_or_create(session, user,
                                               data_point[0], language_code,
                                               data_point[1], "en",
                                               data_point[2], data_point[3], "Zeeguu Exercises")
            bookmarks.append(bookmark)

    except Exception as e:
        zeeguu.log("could not load default bookmarks for {0}".format(language_code))
        #raise e
        return []

    return bookmarks
