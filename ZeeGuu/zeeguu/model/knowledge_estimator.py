from zeeguu.model.bookmark import Bookmark
from zeeguu.model.language import Language
from zeeguu.model.learner_stats.encounter_stats import EncounterStats


class SimpleKnowledgeEstimator(object):
    """
    Computes statistics about this user.
    """

    def __init__(self, user, lang_code=None):
        self.user = user
        if lang_code:
            self.lang_code = lang_code
        else:
            self.lang_code = self.user.learned_language.code
        self.language = Language.find(self.lang_code)

    def get_known_bookmarks(self):
        """
        All the bookmarks that the user knows *and* are in the estimator language
        :param user:
        :param lang:
        :return:
        """
        bookmarks = self.user.all_bookmarks()
        known_bookmarks = []
        for bookmark in bookmarks:
            if bookmark.latest_exercise_outcome():
                if bookmark.latest_exercise_outcome().too_easy() and self.language == bookmark.origin.language:
                    known_bookmark_dict = {
                        'id': bookmark.id,
                        'origin': bookmark.origin.word,
                        'text': bookmark.text.content,
                        'time': bookmark.time.strftime('%m/%d/%Y')}
                    known_bookmarks.append(known_bookmark_dict)
        return known_bookmarks

    def get_known_words(self):
        return [each['origin'] for each in self.get_known_bookmarks()]

    def get_known_bookmarks_count(self):
        return len(self.get_known_bookmarks())

    def get_not_encountered_words(self):
        not_encountered_words = []
        return not_encountered_words

    def get_not_encountered_words_count(self):
        return len(self.get_not_encountered_words())

    # TODO: This must take into account the considered language
    def get_not_looked_up_words(self):
        enc_probs = EncounterStats.find_all(self.user, self.lang_code)
        words = [prob.word_form.word for prob in enc_probs
                 if prob.probability > 0.7]
        return words

    def get_not_looked_up_words_count(self):
        return len(self.get_not_looked_up_words())

    def words_being_learned(self):
        """
            The words the user is currently learning
        :return:
        """
        words_learning = []
        bookmarks = Bookmark.find_by_specific_user(self.user)
        for bookmark in bookmarks:
            learning = False
            if bookmark.latest_exercise_outcome():
                learning = not bookmark.latest_exercise_outcome().too_easy()
            user_word = bookmark.origin
            if learning and user_word.language == self.language:
                words_learning.append(user_word.word)
        return words_learning