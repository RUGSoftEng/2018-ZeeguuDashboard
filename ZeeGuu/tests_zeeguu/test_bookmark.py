import random

from tests_zeeguu.model_test_mixin import ModelTestMixIn

from tests_zeeguu.rules.bookmark_rule import BookmarkRule
from tests_zeeguu.rules.exercise_rule import ExerciseRule
from tests_zeeguu.rules.outcome_rule import OutcomeRule
from tests_zeeguu.rules.source_rule import SourceRule
from tests_zeeguu.rules.text_rule import TextRule
from tests_zeeguu.rules.user_rule import UserRule
from zeeguu.model import Bookmark


class BookmarkTest(ModelTestMixIn):
    def setUp(self):
        super().setUp()

        self.user_rule = UserRule()
        self.user_rule.add_bookmarks(random.randint(1, 3))
        self.user = self.user_rule.user

    def test_add_new_exercise(self):
        random_bookmark = BookmarkRule(self.user).bookmark
        length_original_exercise_log = len(random_bookmark.exercise_log)

        random_exercise = ExerciseRule().exercise
        random_bookmark.add_new_exercise(random_exercise)
        length_new_exercise_log = len(random_bookmark.exercise_log)

        assert length_original_exercise_log < length_new_exercise_log

    def test_translation(self):
        random_bookmark = BookmarkRule(self.user).bookmark
        assert random_bookmark.translation is not None

    def test_bookmarks_in_url(self):
        random_bookmark = BookmarkRule(self.user).bookmark
        url = random_bookmark.text.url
        
        # each bookmark belongs to a random text / url so the
        # combo of user/url will always result in one bookmark
        assert 1 == len(Bookmark.find_all_for_user_and_url(self.user, url))


    def test_text_is_not_too_long(self):
        random_bookmark = BookmarkRule(self.user).bookmark
        random_text_short = TextRule(length=10).text
        random_bookmark.text = random_text_short

        assert random_bookmark.content_is_not_too_long()

        random_text_long = TextRule(length=200).text
        random_bookmark.text = random_text_long

        assert not random_bookmark.content_is_not_too_long()

    def test_add_exercise_outcome(self):
        random_bookmark = BookmarkRule(self.user).bookmark
        random_exercise = ExerciseRule().exercise
        random_bookmark.add_new_exercise_result(random_exercise.source,
                                                random_exercise.outcome,
                                                random_exercise.solving_speed)
        latest_exercise = random_bookmark.exercise_log[-1]

        assert latest_exercise.source == random_exercise.source
        assert latest_exercise.outcome == random_exercise.outcome
        assert latest_exercise.solving_speed == random_exercise.solving_speed

    def test_user_bookmark_count(self):
        assert len(self.user.all_bookmarks()) > 0

    def test_bookmark_is_serializable(self):
        assert self.user.all_bookmarks()[0].json_serializable_dict()

    def test_bad_quality_bookmark(self):
        random_bookmarks = [BookmarkRule(self.user).bookmark for _ in range(0, 3)]

        random_bookmarks[0].origin = random_bookmarks[0].translation
        random_bookmarks[1].origin.word = self.faker.sentence(nb_words=10)
        random_bookmarks[2].origin.word = self.faker.word()[:2]

        for b in random_bookmarks:
            assert b.bad_quality_bookmark()

    def test_fit_for_study(self):
        random_bookmarks = [BookmarkRule(self.user).bookmark for _ in range(0, 2)]
        random_exercise = ExerciseRule().exercise
        random_exercise.outcome = OutcomeRule().correct

        random_bookmarks[0].starred = True
        random_bookmarks[1].starred = True
        random_bookmarks[1].add_new_exercise(random_exercise)

        for b in random_bookmarks:
            assert b.fit_for_study

    def test_add_new_exercise_result(self):
        random_bookmark = BookmarkRule(self.user).bookmark
        exercise_count_before = len(random_bookmark.exercise_log)

        random_bookmark.add_new_exercise_result(SourceRule().random, OutcomeRule().random, random.randint(100, 1000))

        exercise_count_after = len(random_bookmark.exercise_log)

        assert exercise_count_after > exercise_count_before

    def test_find_or_create(self):
        bookmark_should_be = BookmarkRule(self.user).bookmark
        bookmark_to_check = Bookmark.find_or_create(self.db.session, self.user,
                                                    bookmark_should_be.origin.word,
                                                    bookmark_should_be.origin.language.code,
                                                    bookmark_should_be.translation.word,
                                                    bookmark_should_be.translation.language.code,
                                                    bookmark_should_be.text.content, self.faker.uri(),
                                                    self.faker.word())

        assert bookmark_to_check == bookmark_should_be

    def test_find_by_specific_user(self):
        list_should_be = self.user.all_bookmarks()
        list_to_check = Bookmark.find_by_specific_user(self.user)

        for b in list_should_be:
            assert b in list_to_check

    def test_find_all(self):
        list_should_be = self.user.all_bookmarks()
        list_to_check = Bookmark.find_all()

        for b in list_should_be:
            assert b in list_to_check

    def find_all_for_user_and_text(self):
        bookmark_should_be = self.user.all_bookmarks()[0]
        bookmark_to_check = Bookmark.find_all_for_user_and_text(bookmark_should_be.text, self.user)

        assert bookmark_should_be in bookmark_to_check

    def test_find(self):
        bookmark_should_be = self.user.all_bookmarks()[0]
        bookmark_to_check = Bookmark.find(bookmark_should_be.id)

        assert bookmark_to_check == bookmark_should_be

    def test_find_all_by_user_and_word(self):
        bookmark_should_be = self.user.all_bookmarks()[0]
        bookmark_to_check = Bookmark.find_all_by_user_and_word(self.user, bookmark_should_be.origin)

        assert bookmark_should_be in bookmark_to_check

    def test_find_by_user_word_and_text(self):
        bookmark_should_be = self.user.all_bookmarks()[0]
        bookmark_to_check = Bookmark.find_by_user_word_and_text(self.user, bookmark_should_be.origin,
                                                                bookmark_should_be.text)

        assert bookmark_to_check == bookmark_should_be

    def test_exists(self):
        random_bookmark = self.user.all_bookmarks()[0]

        assert Bookmark.exists(random_bookmark)

    def test_latest_exercise_outcome(self):
        random_bookmark = self.user.all_bookmarks()[0]
        assert random_bookmark.latest_exercise_outcome() is None

        random_exercise = ExerciseRule().exercise
        random_bookmark.add_new_exercise(random_exercise)

        assert random_exercise.outcome == random_bookmark.latest_exercise_outcome()

    def test_check_if_learned_based_on_exercise_outcomes(self):
        random_bookmarks = [BookmarkRule(self.user).bookmark for _ in range(0, 4)]

        # Empty exercise_log should lead to a False return
        assert not random_bookmarks[0].check_if_learned_based_on_exercise_outcomes()

        # An exercise with Outcome equal to TOO EASY results in True, and time of last exercise
        random_exercise = ExerciseRule().exercise
        random_exercise.outcome = OutcomeRule().too_easy
        random_bookmarks[1].add_new_exercise(random_exercise)
        result_bool, result_time = random_bookmarks[1].check_if_learned_based_on_exercise_outcomes(
            add_to_result_time=True)
        assert result_bool and result_time == random_exercise.time

        # Same test as above, but without a second return value
        assert random_bookmarks[1].check_if_learned_based_on_exercise_outcomes()

        # A bookmark with 5 correct exercises in a row returns true and the time of the last exercise
        for i in range(0, 5):
            correct_exercise = ExerciseRule().exercise
            correct_exercise.outcome = OutcomeRule().correct
            random_bookmarks[2].add_new_exercise(correct_exercise)

        result_bool, result_time = random_bookmarks[2].check_if_learned_based_on_exercise_outcomes()
        assert result_bool and result_time == random_bookmarks[2].exercise_log[-1].time

        random_bookmarks[2].update_learned_status(self.db.session)

        # A bookmark with no TOO EASY outcome or less than 5 correct exercises in a row returns False, None
        wrong_exercise = ExerciseRule().exercise
        wrong_exercise.outcome = OutcomeRule().wrong
        random_bookmarks[3].add_new_exercise(wrong_exercise)
        result_bool, result_None = random_bookmarks[3].check_if_learned_based_on_exercise_outcomes(
            add_to_result_time=True)
        assert not result_bool and result_None is None

        # Same as before, but without a second return value
        assert not random_bookmarks[3].check_if_learned_based_on_exercise_outcomes()

    def test_has_been_learned(self):
        random_bookmarks = [BookmarkRule(self.user).bookmark for _ in range(0, 2)]

        random_exercise = ExerciseRule().exercise
        random_exercise.outcome = OutcomeRule().too_easy
        random_bookmarks[0].add_new_exercise(random_exercise)
        result_bool, result_time = random_bookmarks[0].has_been_learned(also_return_time=True)
        assert result_bool and result_time == random_bookmarks[0].exercise_log[-1].time

        # TODO: Test the SmartwatchEvent case as well

        result_bool, result_None = random_bookmarks[1].has_been_learned(also_return_time=True)
        assert not result_bool and result_None is None
