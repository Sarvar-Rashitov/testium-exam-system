from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from exams.models import (
    Exam, Section, QuestionGroup,
    MultipleChoiceSingleQuestion, TrueFalseNotGivenQuestion,
    MatchingHeadingsQuestion, HeadingOption,
    SentenceCompletionQuestion, DiagramLabelingQuestion, ImageLabel
)

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a complete sample IELTS Reading exam'

    def handle(self, *args, **kwargs):
        # Get first organization user
        org = User.objects.filter(is_staff=False).first()
        if not org:
            self.stdout.write(self.style.ERROR('No organization user found. Please create one first.'))
            return

        # Create Exam
        exam = Exam.objects.create(
            organization=org,
            title='IELTS Academic Reading Practice Test',
            description='Complete IELTS Academic Reading test with 3 passages and 40 questions',
            duration=60,  # 60 minutes
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS(f'Created exam: {exam.title}'))

        # ==================== SECTION 1: Reading Passage 1 ====================
        section1 = Section.objects.create(
            exam=exam,
            title='Reading Passage 1',
            module='reading',
            order=1,
            passage_text="""THE HISTORY OF BICYCLES

The bicycle is a relatively recent invention. It has existed for less than 200 years. The first bicycle was invented in Germany in 1817 by Baron Karl von Drais. It was called a "running machine" and had no pedals. Riders had to push themselves along with their feet.

In 1839, a Scottish blacksmith named Kirkpatrick Macmillan added pedals to the bicycle. This was a major improvement because riders no longer had to touch the ground. However, Macmillan's bicycle was heavy and difficult to ride.

The next important development came in the 1860s when French inventors Pierre and Ernest Michaux attached pedals directly to the front wheel. This design became very popular and was known as the "velocipede" or "boneshaker" because of its uncomfortable ride on rough roads.

In 1870, the "penny-farthing" bicycle was introduced. It had a very large front wheel and a small rear wheel. This design allowed riders to travel faster, but it was dangerous. Riders sat high above the ground and could easily fall forward over the handlebars.

The modern bicycle design appeared in the 1880s. It featured two wheels of equal size, a chain drive, and pneumatic (air-filled) tires. This design, called the "safety bicycle," was much more stable and comfortable than earlier versions. By 1900, the bicycle had become a popular form of transportation around the world.

Today, bicycles are used for transportation, recreation, and sport. They are environmentally friendly and provide good exercise. Modern bicycles incorporate advanced materials and technology, but the basic design has remained largely unchanged for over a century.""",
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS(f'Created section: {section1.title}'))

        # Question Group 1: Multiple Choice
        group1 = QuestionGroup.objects.create(
            section=section1,
            question_type='multiple_choice_single',
            title='Questions 1-4',
            instructions='Choose the correct letter, A, B, C or D.',
            order=1
        )

        questions_mc = [
            {
                'number': 1,
                'text': 'The first bicycle was invented in',
                'a': '1817',
                'b': '1839',
                'c': '1860',
                'd': '1870',
                'answer': 'A'
            },
            {
                'number': 2,
                'text': 'Who added pedals to the bicycle?',
                'a': 'Baron Karl von Drais',
                'b': 'Kirkpatrick Macmillan',
                'c': 'Pierre Michaux',
                'd': 'Ernest Michaux',
                'answer': 'B'
            },
            {
                'number': 3,
                'text': 'The "boneshaker" was uncomfortable because',
                'a': 'it had no pedals',
                'b': 'it was too heavy',
                'c': 'of rough roads',
                'd': 'riders sat too high',
                'answer': 'C'
            },
            {
                'number': 4,
                'text': 'The modern bicycle design appeared in the',
                'a': '1860s',
                'b': '1870s',
                'c': '1880s',
                'd': '1900s',
                'answer': 'C'
            }
        ]

        for q in questions_mc:
            MultipleChoiceSingleQuestion.objects.create(
                question_group=group1,
                question_number=q['number'],
                question_text=q['text'],
                option_a=q['a'],
                option_b=q['b'],
                option_c=q['c'],
                option_d=q['d'],
                correct_answer=q['answer'],
                points=1
            )

        # Question Group 2: True/False/Not Given
        group2 = QuestionGroup.objects.create(
            section=section1,
            question_type='true_false_ng',
            title='Questions 5-8',
            instructions='Do the following statements agree with the information in the passage? Write TRUE, FALSE or NOT GIVEN.',
            order=2
        )

        questions_tf = [
            {
                'number': 5,
                'statement': 'The first bicycle had pedals.',
                'answer': 'FALSE'
            },
            {
                'number': 6,
                'statement': 'Macmillan\'s bicycle was easy to ride.',
                'answer': 'FALSE'
            },
            {
                'number': 7,
                'statement': 'The penny-farthing was a safe bicycle.',
                'answer': 'FALSE'
            },
            {
                'number': 8,
                'statement': 'Modern bicycles are more expensive than old bicycles.',
                'answer': 'NOT GIVEN'
            }
        ]

        for q in questions_tf:
            TrueFalseNotGivenQuestion.objects.create(
                question_group=group2,
                question_number=q['number'],
                statement=q['statement'],
                correct_answer=q['answer'],
                points=1
            )

        # Question Group 3: Sentence Completion
        group3 = QuestionGroup.objects.create(
            section=section1,
            question_type='sentence_completion',
            title='Questions 9-13',
            instructions='Complete the sentences below. Write NO MORE THAN TWO WORDS from the passage for each answer.',
            order=3
        )

        questions_sc = [
            {
                'number': 9,
                'text': 'The first bicycle was called a _____.',
                'answer': 'running machine'
            },
            {
                'number': 10,
                'text': 'The velocipede was also known as the _____.',
                'answer': 'boneshaker'
            },
            {
                'number': 11,
                'text': 'The safety bicycle had _____ tires.',
                'answer': 'pneumatic'
            },
            {
                'number': 12,
                'text': 'Bicycles are _____ friendly.',
                'answer': 'environmentally'
            },
            {
                'number': 13,
                'text': 'The basic bicycle design has remained _____ for over a century.',
                'answer': 'unchanged'
            }
        ]

        for q in questions_sc:
            SentenceCompletionQuestion.objects.create(
                question_group=group3,
                question_number=q['number'],
                sentence_text=q['text'],
                correct_answer=q['answer'],
                max_words=2,
                points=1
            )

        # ==================== SECTION 2: Reading Passage 2 ====================
        section2 = Section.objects.create(
            exam=exam,
            title='Reading Passage 2',
            module='reading',
            order=2,
            passage_text="""CLIMATE CHANGE AND ITS EFFECTS

A. Climate change refers to long-term shifts in global temperatures and weather patterns. While climate change is a natural phenomenon, scientific evidence shows that human activities have been the main driver of climate change since the mid-20th century, primarily due to the burning of fossil fuels like coal, oil, and gas.

B. The effects of climate change are already visible around the world. Global temperatures have risen by approximately 1.1°C since the pre-industrial era. This warming has led to melting ice caps and glaciers, rising sea levels, and more frequent extreme weather events such as hurricanes, droughts, and floods.

C. One of the most significant impacts of climate change is on biodiversity. Many species are struggling to adapt to rapidly changing conditions. Coral reefs, which support 25% of all marine species, are particularly vulnerable. Rising ocean temperatures cause coral bleaching, which can lead to the death of entire reef systems.

D. Climate change also affects human health. Higher temperatures can lead to heat-related illnesses and deaths. Changes in weather patterns can affect the spread of infectious diseases. Air pollution from burning fossil fuels contributes to respiratory problems and cardiovascular disease.

E. Agriculture is another sector heavily impacted by climate change. Changes in temperature and precipitation patterns affect crop yields. Some regions may become too dry for farming, while others may experience increased flooding. This threatens food security, particularly in developing countries.

F. Despite these challenges, there are solutions. Reducing greenhouse gas emissions is crucial. This can be achieved through renewable energy sources like solar and wind power, improving energy efficiency, and protecting forests. Individual actions, such as reducing consumption and choosing sustainable products, also make a difference.

G. International cooperation is essential to address climate change. The Paris Agreement, signed by 196 countries in 2015, aims to limit global warming to well below 2°C above pre-industrial levels. However, current commitments are not sufficient to meet this goal, and more ambitious action is needed.""",
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS(f'Created section: {section2.title}'))

        # Question Group 4: Matching Headings
        group4 = QuestionGroup.objects.create(
            section=section2,
            question_type='matching_headings',
            title='Questions 14-20',
            instructions='The passage has seven paragraphs, A-G. Choose the correct heading for each paragraph from the list of headings below.',
            order=1
        )

        # Add heading options
        headings = [
            ('i', 'The impact on food production'),
            ('ii', 'What is causing the problem'),
            ('iii', 'Effects on ocean ecosystems'),
            ('iv', 'International efforts to combat climate change'),
            ('v', 'Health consequences of climate change'),
            ('vi', 'Observable changes in the environment'),
            ('vii', 'Possible ways to address the issue'),
            ('viii', 'Economic impacts of climate change'),
            ('ix', 'The role of technology in climate change'),
        ]

        for label, text in headings:
            HeadingOption.objects.create(
                question_group=group4,
                heading_label=label,
                heading_text=text,
                order=int(label[1:]) if label[1:].isdigit() else 0
            )

        # Add matching questions
        paragraph_headings = [
            {'number': 14, 'paragraph': 'A', 'heading': 'ii'},
            {'number': 15, 'paragraph': 'B', 'heading': 'vi'},
            {'number': 16, 'paragraph': 'C', 'heading': 'iii'},
            {'number': 17, 'paragraph': 'D', 'heading': 'v'},
            {'number': 18, 'paragraph': 'E', 'heading': 'i'},
            {'number': 19, 'paragraph': 'F', 'heading': 'vii'},
            {'number': 20, 'paragraph': 'G', 'heading': 'iv'},
        ]

        for q in paragraph_headings:
            MatchingHeadingsQuestion.objects.create(
                question_group=group4,
                question_number=q['number'],
                paragraph_label=q['paragraph'],
                correct_heading=q['heading'],
                points=1
            )

        # Question Group 5: Multiple Choice
        group5 = QuestionGroup.objects.create(
            section=section2,
            question_type='multiple_choice_single',
            title='Questions 21-26',
            instructions='Choose the correct letter, A, B, C or D.',
            order=2
        )

        questions_mc2 = [
            {
                'number': 21,
                'text': 'According to the passage, the main cause of recent climate change is',
                'a': 'natural phenomena',
                'b': 'human activities',
                'c': 'volcanic eruptions',
                'd': 'solar radiation',
                'answer': 'B'
            },
            {
                'number': 22,
                'text': 'Global temperatures have increased by approximately',
                'a': '0.5°C',
                'b': '1.1°C',
                'c': '2.0°C',
                'd': '3.0°C',
                'answer': 'B'
            },
            {
                'number': 23,
                'text': 'Coral reefs support what percentage of marine species?',
                'a': '10%',
                'b': '15%',
                'c': '25%',
                'd': '50%',
                'answer': 'C'
            },
            {
                'number': 24,
                'text': 'The Paris Agreement was signed in',
                'a': '2010',
                'b': '2015',
                'c': '2020',
                'd': '2025',
                'answer': 'B'
            },
            {
                'number': 25,
                'text': 'The Paris Agreement aims to limit warming to',
                'a': 'below 1°C',
                'b': 'below 1.5°C',
                'c': 'below 2°C',
                'd': 'below 3°C',
                'answer': 'C'
            },
            {
                'number': 26,
                'text': 'According to the passage, which is NOT mentioned as a solution?',
                'a': 'Renewable energy',
                'b': 'Nuclear power',
                'c': 'Protecting forests',
                'd': 'Improving energy efficiency',
                'answer': 'B'
            }
        ]

        for q in questions_mc2:
            MultipleChoiceSingleQuestion.objects.create(
                question_group=group5,
                question_number=q['number'],
                question_text=q['text'],
                option_a=q['a'],
                option_b=q['b'],
                option_c=q['c'],
                option_d=q['d'],
                correct_answer=q['answer'],
                points=1
            )

        # ==================== SECTION 3: Reading Passage 3 ====================
        section3 = Section.objects.create(
            exam=exam,
            title='Reading Passage 3',
            module='reading',
            order=3,
            passage_text="""THE SCIENCE OF SLEEP

Sleep is a fundamental biological process that is essential for human health and well-being. Despite spending approximately one-third of our lives asleep, the exact purpose of sleep remains one of the great mysteries of science. However, research has revealed many important functions that sleep serves.

During sleep, the brain goes through several distinct stages, each characterized by different patterns of brain activity. These stages are divided into two main categories: non-rapid eye movement (NREM) sleep and rapid eye movement (REM) sleep. NREM sleep consists of three stages, progressing from light sleep to deep sleep. REM sleep is the stage during which most dreaming occurs.

One of the most important functions of sleep is memory consolidation. During sleep, particularly during deep NREM sleep and REM sleep, the brain processes and stores information acquired during the day. Studies have shown that people who get adequate sleep after learning new information perform better on memory tests than those who are sleep-deprived.

Sleep also plays a crucial role in physical health. During deep sleep, the body repairs tissues, builds muscle, and strengthens the immune system. Growth hormone, which is essential for development in children and tissue repair in adults, is primarily released during deep sleep. Lack of sleep has been linked to various health problems, including obesity, diabetes, cardiovascular disease, and weakened immunity.

The amount of sleep needed varies by age and individual. Newborns require 14-17 hours of sleep per day, while adults typically need 7-9 hours. However, sleep quality is just as important as quantity. Factors that affect sleep quality include the sleep environment, stress levels, diet, and exercise habits.

In modern society, many people suffer from chronic sleep deprivation. The widespread use of electronic devices, particularly before bedtime, has been identified as a major contributor to sleep problems. The blue light emitted by screens can suppress the production of melatonin, a hormone that regulates sleep-wake cycles, making it harder to fall asleep.

Sleep disorders affect millions of people worldwide. Insomnia, characterized by difficulty falling or staying asleep, is the most common sleep disorder. Sleep apnea, a condition in which breathing repeatedly stops and starts during sleep, affects approximately 5-10% of adults. Other sleep disorders include narcolepsy, restless leg syndrome, and circadian rhythm disorders.

Improving sleep hygiene can help many people get better sleep. This includes maintaining a consistent sleep schedule, creating a comfortable sleep environment, avoiding caffeine and alcohol before bedtime, and limiting screen time in the evening. For those with persistent sleep problems, consulting a healthcare provider or sleep specialist is recommended.""",
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS(f'Created section: {section3.title}'))

        # Question Group 6: True/False/Not Given
        group6 = QuestionGroup.objects.create(
            section=section3,
            question_type='true_false_ng',
            title='Questions 27-32',
            instructions='Do the following statements agree with the information in the passage? Write TRUE, FALSE or NOT GIVEN.',
            order=1
        )

        questions_tf2 = [
            {
                'number': 27,
                'statement': 'Scientists fully understand why humans need to sleep.',
                'answer': 'FALSE'
            },
            {
                'number': 28,
                'statement': 'Most dreaming occurs during REM sleep.',
                'answer': 'TRUE'
            },
            {
                'number': 29,
                'statement': 'Sleep-deprived people perform worse on memory tests.',
                'answer': 'TRUE'
            },
            {
                'number': 30,
                'statement': 'Growth hormone is only important for children.',
                'answer': 'FALSE'
            },
            {
                'number': 31,
                'statement': 'All adults need exactly 8 hours of sleep.',
                'answer': 'FALSE'
            },
            {
                'number': 32,
                'statement': 'Sleep apnea is more common in women than men.',
                'answer': 'NOT GIVEN'
            }
        ]

        for q in questions_tf2:
            TrueFalseNotGivenQuestion.objects.create(
                question_group=group6,
                question_number=q['number'],
                statement=q['statement'],
                correct_answer=q['answer'],
                points=1
            )

        # Question Group 7: Sentence Completion
        group7 = QuestionGroup.objects.create(
            section=section3,
            question_type='sentence_completion',
            title='Questions 33-40',
            instructions='Complete the sentences below. Write NO MORE THAN THREE WORDS from the passage for each answer.',
            order=2
        )

        questions_sc2 = [
            {
                'number': 33,
                'text': 'Sleep stages are divided into NREM sleep and _____.',
                'answer': 'REM sleep'
            },
            {
                'number': 34,
                'text': 'Memory consolidation occurs during deep NREM sleep and _____.',
                'answer': 'REM sleep'
            },
            {
                'number': 35,
                'text': 'During deep sleep, the body repairs tissues and strengthens the _____.',
                'answer': 'immune system'
            },
            {
                'number': 36,
                'text': 'Newborns require _____ hours of sleep per day.',
                'answer': '14-17'
            },
            {
                'number': 37,
                'text': 'Blue light from screens can suppress the production of _____.',
                'answer': 'melatonin'
            },
            {
                'number': 38,
                'text': 'The most common sleep disorder is _____.',
                'answer': 'insomnia'
            },
            {
                'number': 39,
                'text': 'Sleep apnea affects approximately _____ of adults.',
                'answer': '5-10%'
            },
            {
                'number': 40,
                'text': 'Improving _____ can help people get better sleep.',
                'answer': 'sleep hygiene'
            }
        ]

        for q in questions_sc2:
            SentenceCompletionQuestion.objects.create(
                question_group=group7,
                question_number=q['number'],
                sentence_text=q['text'],
                correct_answer=q['answer'],
                max_words=3,
                points=1
            )

        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(self.style.SUCCESS(f'Successfully created complete IELTS exam!'))
        self.stdout.write(self.style.SUCCESS(f'Exam ID: {exam.id}'))
        self.stdout.write(self.style.SUCCESS(f'Total Sections: 3'))
        self.stdout.write(self.style.SUCCESS(f'Total Questions: 40'))
        self.stdout.write(self.style.SUCCESS('='*50))
