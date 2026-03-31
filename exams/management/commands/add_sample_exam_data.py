from django.core.management.base import BaseCommand
from exams.models import (
    Exam, Section, QuestionGroup,
    MultipleChoiceSingleQuestion, TrueFalseNotGivenQuestion,
    YesNoNotGivenQuestion, SentenceCompletionQuestion,
    ShortAnswerQuestion
)


class Command(BaseCommand):
    help = 'Add sample exam data to exam with ID 3'

    def handle(self, *args, **kwargs):
        try:
            exam = Exam.objects.get(id=3)
        except Exam.DoesNotExist:
            self.stdout.write(self.style.ERROR('Exam with ID 3 does not exist!'))
            return

        self.stdout.write(self.style.SUCCESS(f'Adding sample data to exam: {exam.title}'))

        # Create Reading Section
        reading_section = Section.objects.create(
            exam=exam,
            title='Reading Section 1',
            module='reading',
            order=1,
            passage_text="""The History of Coffee

Coffee is one of the most popular beverages in the world. The coffee plant, from which coffee beans are harvested, is believed to have originated in Ethiopia. According to legend, a goat herder named Kaldi discovered coffee after noticing that his goats became energetic after eating berries from a certain tree.

The cultivation and trade of coffee began on the Arabian Peninsula. By the 15th century, coffee was being grown in Yemen, and by the 16th century, it had spread to Persia, Egypt, Syria, and Turkey. Coffee houses, called "qahveh khaneh," began appearing in cities across the Near East. These establishments became important centers for social activity and communication.

Coffee came to Europe in the 17th century and quickly became popular, though it was initially met with suspicion and was even called "the bitter invention of Satan" by some. Pope Clement VIII is said to have tasted coffee and given it papal approval, which helped its acceptance. By the mid-17th century, there were over 300 coffee houses in London alone.

The Dutch were the first to transport and cultivate coffee commercially, in Ceylon (now Sri Lanka) and later in Java. Through the efforts of the British East India Company, coffee became popular in England as well. Coffee houses were established and quickly became centers of social activity and communication in the major cities of England.

Today, coffee is grown in numerous countries around the world, with Brazil being the largest producer. The coffee industry employs millions of people worldwide and continues to be an important part of the global economy."""
        )

        # Create Question Group 1 - Multiple Choice
        group1 = QuestionGroup.objects.create(
            section=reading_section,
            question_type='multiple_choice_single',
            title='Questions 1-5',
            instructions='Choose the correct letter, A, B, C or D.',
            order=1
        )

        # Add Multiple Choice Questions
        MultipleChoiceSingleQuestion.objects.create(
            question_group=group1,
            question_number=1,
            question_text='According to the passage, where did coffee originate?',
            option_a='Yemen',
            option_b='Ethiopia',
            option_c='Arabia',
            option_d='Turkey',
            correct_answer='B',
            points=1
        )

        MultipleChoiceSingleQuestion.objects.create(
            question_group=group1,
            question_number=2,
            question_text='Who is believed to have discovered coffee?',
            option_a='A farmer',
            option_b='A trader',
            option_c='A goat herder named Kaldi',
            option_d='Pope Clement VIII',
            correct_answer='C',
            points=1
        )

        MultipleChoiceSingleQuestion.objects.create(
            question_group=group1,
            question_number=3,
            question_text='By which century was coffee being grown in Yemen?',
            option_a='14th century',
            option_b='15th century',
            option_c='16th century',
            option_d='17th century',
            correct_answer='B',
            points=1
        )

        MultipleChoiceSingleQuestion.objects.create(
            question_group=group1,
            question_number=4,
            question_text='What were coffee houses in the Near East called?',
            option_a='Cafes',
            option_b='Qahveh khaneh',
            option_c='Coffee shops',
            option_d='Tea houses',
            correct_answer='B',
            points=1
        )

        MultipleChoiceSingleQuestion.objects.create(
            question_group=group1,
            question_number=5,
            question_text='Which country is currently the largest coffee producer?',
            option_a='Colombia',
            option_b='Vietnam',
            option_c='Brazil',
            option_d='Ethiopia',
            correct_answer='C',
            points=1
        )

        # Create Question Group 2 - True/False/Not Given
        group2 = QuestionGroup.objects.create(
            section=reading_section,
            question_type='true_false_ng',
            title='Questions 6-10',
            instructions='Do the following statements agree with the information in the passage? Write TRUE, FALSE or NOT GIVEN.',
            order=2
        )

        TrueFalseNotGivenQuestion.objects.create(
            question_group=group2,
            question_number=6,
            statement='Coffee was initially welcomed in Europe without any suspicion.',
            correct_answer='FALSE',
            points=1
        )

        TrueFalseNotGivenQuestion.objects.create(
            question_group=group2,
            question_number=7,
            statement='Pope Clement VIII approved coffee for consumption.',
            correct_answer='TRUE',
            points=1
        )

        TrueFalseNotGivenQuestion.objects.create(
            question_group=group2,
            question_number=8,
            statement='There were exactly 300 coffee houses in London by the mid-17th century.',
            correct_answer='FALSE',
            points=1
        )

        TrueFalseNotGivenQuestion.objects.create(
            question_group=group2,
            question_number=9,
            statement='The Dutch were the first to cultivate coffee commercially.',
            correct_answer='TRUE',
            points=1
        )

        TrueFalseNotGivenQuestion.objects.create(
            question_group=group2,
            question_number=10,
            statement='Coffee cultivation requires specific climate conditions.',
            correct_answer='NOT GIVEN',
            points=1
        )

        # Create Question Group 3 - Sentence Completion
        group3 = QuestionGroup.objects.create(
            section=reading_section,
            question_type='sentence_completion',
            title='Questions 11-13',
            instructions='Complete the sentences below. Write NO MORE THAN THREE WORDS from the passage for each answer.',
            order=3
        )

        SentenceCompletionQuestion.objects.create(
            question_group=group3,
            question_number=11,
            sentence_text='Kaldi noticed his goats became _____ after eating coffee berries.',
            correct_answer='energetic',
            alternative_answers='',
            max_words=1,
            points=1
        )

        SentenceCompletionQuestion.objects.create(
            question_group=group3,
            question_number=12,
            sentence_text='Coffee houses became important centers for _____ and communication.',
            correct_answer='social activity',
            alternative_answers='',
            max_words=2,
            points=1
        )

        SentenceCompletionQuestion.objects.create(
            question_group=group3,
            question_number=13,
            sentence_text='The coffee industry employs _____ of people worldwide.',
            correct_answer='millions',
            alternative_answers='',
            max_words=1,
            points=1
        )

        # Create Listening Section
        listening_section = Section.objects.create(
            exam=exam,
            title='Listening Section 1',
            module='listening',
            order=2,
            audio_url='https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3'
        )

        # Create Question Group 4 - Short Answer
        group4 = QuestionGroup.objects.create(
            section=listening_section,
            question_type='short_answer',
            title='Questions 14-17',
            instructions='Answer the questions below. Write NO MORE THAN THREE WORDS AND/OR A NUMBER for each answer.',
            order=1
        )

        ShortAnswerQuestion.objects.create(
            question_group=group4,
            question_number=14,
            question_text='What is the speaker\'s name?',
            correct_answer='John Smith',
            alternative_answers='',
            max_words=3,
            points=1
        )

        ShortAnswerQuestion.objects.create(
            question_group=group4,
            question_number=15,
            question_text='What time does the library open?',
            correct_answer='9 AM',
            alternative_answers='9:00 AM\n9 o\'clock',
            max_words=3,
            points=1
        )

        ShortAnswerQuestion.objects.create(
            question_group=group4,
            question_number=16,
            question_text='How many books can students borrow?',
            correct_answer='5',
            alternative_answers='five',
            max_words=1,
            points=1
        )

        ShortAnswerQuestion.objects.create(
            question_group=group4,
            question_number=17,
            question_text='Where is the computer lab located?',
            correct_answer='second floor',
            alternative_answers='2nd floor',
            max_words=2,
            points=1
        )

        # Create Question Group 5 - Yes/No/Not Given
        group5 = QuestionGroup.objects.create(
            section=listening_section,
            question_type='yes_no_ng',
            title='Questions 18-20',
            instructions='Do the following statements agree with the views of the speaker? Write YES, NO or NOT GIVEN.',
            order=2
        )

        YesNoNotGivenQuestion.objects.create(
            question_group=group5,
            question_number=18,
            statement='The library has a good collection of science books.',
            correct_answer='YES',
            points=1
        )

        YesNoNotGivenQuestion.objects.create(
            question_group=group5,
            question_number=19,
            statement='Students need to pay a fee to use the library.',
            correct_answer='NO',
            points=1
        )

        YesNoNotGivenQuestion.objects.create(
            question_group=group5,
            question_number=20,
            statement='The library will be renovated next year.',
            correct_answer='NOT GIVEN',
            points=1
        )

        self.stdout.write(self.style.SUCCESS(f'Successfully added sample data to exam ID 3'))
        self.stdout.write(self.style.SUCCESS(f'Total questions added: 20'))
        self.stdout.write(self.style.SUCCESS(f'- Reading Section: 13 questions'))
        self.stdout.write(self.style.SUCCESS(f'- Listening Section: 7 questions'))
