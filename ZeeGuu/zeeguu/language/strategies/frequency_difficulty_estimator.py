from wordstats import Word, WordInfo
from zeeguu import model
from zeeguu.language.difficulty_estimator_strategy import DifficultyEstimatorStrategy
from zeeguu.util.text import split_words_from_text


class FrequencyDifficultyEstimator(DifficultyEstimatorStrategy):

    CUSTOM_NAMES = ["frequency"]

    @classmethod
    def estimate_difficulty(cls, text: str, language: 'model.Language', user: 'model.User'):
        """
        This estimator computes the difficulty based on how often words in the text are used in the given language
        :param text: See DifficultyEstimatorStrategy
        :param language: See DifficultyEstimatorStrategy
        :param user: See DifficultyEstimatorStrategy
        :rtype: dict
        :return: The dictionary contains the keys and return types
                    normalized: float (0<=normalized<=1)
                    discrete: string [EASY, MEDIUM, HARD]
        """
        word_difficulties = []

        # Calculate difficulty for each word
        words = split_words_from_text(text)
        for word in words:
            difficulty = cls.word_difficulty({}, True, Word.stats(word, language.code), word)
            word_difficulties.append(difficulty)

        # If we can't compute the text difficulty, we estimate hard
        if (len(word_difficulties)) == 0:
            normalized_estimate = 0.35
            discrete_difficulty = "MEDIUM"
        else:
            # Median difficulty is used for discretization
            word_difficulties.sort()
            center = int(round(len(word_difficulties) / 2, 0))
            difficulty_median = word_difficulties[center]

            normalized_estimate = sum(word_difficulties) / float(len(word_difficulties))
            discrete_difficulty = cls.discrete_text_difficulty(difficulty_median)

        difficulty_scores = dict(
            normalized=normalized_estimate,             # Originally called 'score_average'
            discrete=discrete_difficulty                # Originally called 'estimated_difficulty'
        )

        return difficulty_scores

    @classmethod
    def discrete_text_difficulty(cls, median_difficulty: float):
        """
        :param median_difficulty:
        :return: a symbolic representation of the estimated difficulty
         the values are between "EASY", "MEDIUM", and "HARD"
        """
        if median_difficulty < 0.3:
            return "EASY"
        if median_difficulty < 0.4:
            return "MEDIUM"
        return "HARD"

    @classmethod
    # TODO: must test this thing
    def word_difficulty(cls, known_probabilities: dict, personalized: bool, word_info: WordInfo, word: Word):
        """
        # estimate the difficulty of a word, given:
            :param word_info:
            :param known_probabilities:
            :param personalized:
            :param word:

        :return: a normalized value where 0 is (easy) and 1 is (hard)
        """

        # Assume word is difficult and unknown
        estimated_difficulty = 1.0

        # Check if the user knows the word
        try:
            known_probability = known_probabilities[word]  # Value between 0 (unknown) and 1 (known)
        except KeyError:
            known_probability = None

        if personalized and known_probability is not None:
            estimated_difficulty -= float(known_probability)
        elif word_info:
            estimated_difficulty = word_info.difficulty

        return estimated_difficulty

