from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from exams.models import (
    Exam, Section, QuestionGroup,
    MultipleChoiceSingleQuestion, MultipleChoiceMultipleQuestion,
    TrueFalseNotGivenQuestion, YesNoNotGivenQuestion,
    SentenceCompletionQuestion, ShortAnswerQuestion,
    DiagramLabelingQuestion, ImageLabel, SummaryCompletionQuestion,
    NoteCompletionQuestion, TableCompletionQuestion,
    FlowchartCompletionQuestion, MatchingHeadingsQuestion, HeadingOption,
    MatchingInformationQuestion, MatchingFeaturesQuestion, FeatureOption,
    MatchingSentenceEndingsQuestion, SentenceEndingOption
)

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a complete exam with ALL question types for testing'

    def handle(self, *args, **kwargs):
        # Get first organization user
        org = User.objects.filter(is_staff=False).first()
        if not org:
            self.stdout.write(self.style.ERROR('No organization user found. Please create one first.'))
            return

        # Create Exam
        exam = Exam.objects.create(
            organization=org,
            title='Complete IELTS Test - All Question Types',
            description='Comprehensive test covering all 15 IELTS question types',
            duration=90,  # 90 minutes
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS(f'✓ Created exam: {exam.title}'))

        # ==================== SECTION 1: Multiple Choice & True/False ====================
        section1 = Section.objects.create(
            exam=exam,
            title='Section 1: Multiple Choice & True/False Questions',
            module='reading',
            order=1,
            passage_text="""ARTIFICIAL INTELLIGENCE IN HEALTHCARE

Artificial Intelligence (AI) is revolutionizing healthcare in numerous ways. Machine learning algorithms can now analyze medical images with accuracy comparable to human radiologists. AI systems can detect patterns in patient data that might be missed by human doctors, leading to earlier diagnosis of diseases.

One of the most promising applications of AI in healthcare is in drug discovery. Traditional drug development can take over a decade and cost billions of dollars. AI can analyze vast amounts of biological data to identify potential drug candidates much faster, potentially reducing both time and cost.

AI-powered chatbots and virtual assistants are also improving patient care. These systems can answer common medical questions, schedule appointments, and even provide preliminary diagnoses based on symptoms. This helps reduce the workload on healthcare professionals and provides patients with immediate access to medical information.

However, there are concerns about AI in healthcare. Privacy and security of patient data is a major issue. There are also questions about liability when AI systems make mistakes. Additionally, some worry that AI might replace human healthcare workers, though most experts believe AI will augment rather than replace human doctors.""",
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS(f'✓ Created section: {section1.title}'))

        # Group 1: Multiple Choice Single
        group1 = QuestionGroup.objects.create(
            section=section1,
            question_type='multiple_choice_single',
            title='Questions 1-3: Multiple Choice (Single Answer)',
            instructions='Choose the correct letter, A, B, C or D.',
            order=1
        )

        mc_single = [
            {
                'num': 1,
                'text': 'AI in healthcare can analyze medical images with accuracy',
                'a': 'better than human radiologists',
                'b': 'comparable to human radiologists',
                'c': 'worse than human radiologists',
                'd': 'not mentioned in the passage',
                'answer': 'B'
            },
            {
                'num': 2,
                'text': 'Traditional drug development can take',
                'a': 'over 5 years',
                'b': 'over 10 years',
                'c': 'over 20 years',
                'd': 'over 50 years',
                'answer': 'B'
            },
            {
                'num': 3,
                'text': 'Most experts believe AI will',
                'a': 'replace human doctors',
                'b': 'be rejected by doctors',
                'c': 'augment human doctors',
                'd': 'be too expensive',
                'answer': 'C'
            }
        ]

        for q in mc_single:
            MultipleChoiceSingleQuestion.objects.create(
                question_group=group1,
                question_number=q['num'],
                question_text=q['text'],
                option_a=q['a'],
                option_b=q['b'],
                option_c=q['c'],
                option_d=q['d'],
                correct_answer=q['answer'],
                points=1
            )

        # Group 2: Multiple Choice Multiple
        group2 = QuestionGroup.objects.create(
            section=section1,
            question_type='multiple_choice_multiple',
            title='Questions 4-5: Multiple Choice (Multiple Answers)',
            instructions='Choose TWO letters, A-E.',
            order=2
        )

        mc_multiple = [
            {
                'num': 4,
                'text': 'Which TWO concerns about AI in healthcare are mentioned?',
                'a': 'Privacy and security',
                'b': 'High cost',
                'c': 'Liability issues',
                'd': 'Slow processing',
                'e': 'Language barriers',
                'answer': 'A,C'
            },
            {
                'num': 5,
                'text': 'Which TWO applications of AI in healthcare are mentioned?',
                'a': 'Surgery robots',
                'b': 'Medical image analysis',
                'c': 'Drug discovery',
                'd': 'Vaccine development',
                'e': 'Hospital management',
                'answer': 'B,C'
            }
        ]

        for q in mc_multiple:
            MultipleChoiceMultipleQuestion.objects.create(
                question_group=group2,
                question_number=q['num'],
                question_text=q['text'],
                option_a=q['a'],
                option_b=q['b'],
                option_c=q['c'],
                option_d=q['d'],
                option_e=q['e'],
                correct_answers=q['answer'],
                points=1
            )

        # Group 3: True/False/Not Given
        group3 = QuestionGroup.objects.create(
            section=section1,
            question_type='true_false_ng',
            title='Questions 6-8: True/False/Not Given',
            instructions='Write TRUE, FALSE or NOT GIVEN.',
            order=3
        )

        tf_questions = [
            {'num': 6, 'statement': 'AI can detect patterns that human doctors might miss.', 'answer': 'TRUE'},
            {'num': 7, 'statement': 'AI chatbots can perform surgery.', 'answer': 'NOT GIVEN'},
            {'num': 8, 'statement': 'Drug development traditionally costs billions of dollars.', 'answer': 'TRUE'}
        ]

        for q in tf_questions:
            TrueFalseNotGivenQuestion.objects.create(
                question_group=group3,
                question_number=q['num'],
                statement=q['statement'],
                correct_answer=q['answer'],
                points=1
            )

        # Group 4: Yes/No/Not Given
        group4 = QuestionGroup.objects.create(
            section=section1,
            question_type='yes_no_ng',
            title='Questions 9-10: Yes/No/Not Given',
            instructions='Write YES, NO or NOT GIVEN.',
            order=4
        )

        yn_questions = [
            {'num': 9, 'statement': 'The author believes AI will completely replace doctors.', 'answer': 'NO'},
            {'num': 10, 'statement': 'AI chatbots reduce workload on healthcare professionals.', 'answer': 'YES'}
        ]

        for q in yn_questions:
            YesNoNotGivenQuestion.objects.create(
                question_group=group4,
                question_number=q['num'],
                statement=q['statement'],
                correct_answer=q['answer'],
                points=1
            )

        # ==================== SECTION 2: Completion Questions ====================
        section2 = Section.objects.create(
            exam=exam,
            title='Section 2: Completion Questions',
            module='reading',
            order=2,
            passage_text="""RENEWABLE ENERGY SOURCES

Solar power is one of the fastest-growing renewable energy sources. Solar panels convert sunlight directly into electricity through photovoltaic cells. The efficiency of solar panels has improved dramatically over the past decade, making them more cost-effective.

Wind energy is another major renewable source. Wind turbines convert the kinetic energy of wind into electrical power. Modern wind farms can generate enough electricity to power thousands of homes. Offshore wind farms are particularly effective because ocean winds are stronger and more consistent.

Hydroelectric power has been used for over a century. It generates electricity by using flowing water to turn turbines. Large dams can produce enormous amounts of power, but they can also have significant environmental impacts on river ecosystems.

Geothermal energy harnesses heat from beneath the Earth's surface. This heat can be used directly for heating buildings or converted into electricity. Geothermal power plants are most common in areas with volcanic activity, such as Iceland and New Zealand.

Biomass energy comes from organic materials like wood, crops, and waste. When burned or converted into biofuels, these materials release energy that can be used for heating or electricity generation. However, the sustainability of biomass depends on how the organic materials are sourced.""",
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS(f'✓ Created section: {section2.title}'))

        # Group 5: Sentence Completion
        group5 = QuestionGroup.objects.create(
            section=section2,
            question_type='sentence_completion',
            title='Questions 11-15: Sentence Completion',
            instructions='Complete the sentences. Write NO MORE THAN TWO WORDS from the passage.',
            order=1
        )

        sentence_comp = [
            {'num': 11, 'text': 'Solar panels convert sunlight into electricity through _____.', 'answer': 'photovoltaic cells'},
            {'num': 12, 'text': 'Offshore wind farms are effective because ocean winds are stronger and more _____.', 'answer': 'consistent'},
            {'num': 13, 'text': 'Hydroelectric power uses flowing water to turn _____.', 'answer': 'turbines'},
            {'num': 14, 'text': 'Geothermal power plants are common in areas with _____ activity.', 'answer': 'volcanic'},
            {'num': 15, 'text': 'Biomass energy comes from _____ materials.', 'answer': 'organic'}
        ]

        for q in sentence_comp:
            SentenceCompletionQuestion.objects.create(
                question_group=group5,
                question_number=q['num'],
                sentence_text=q['text'],
                correct_answer=q['answer'],
                max_words=2,
                points=1
            )

        # Group 6: Summary Completion
        group6 = QuestionGroup.objects.create(
            section=section2,
            question_type='summary_completion',
            title='Questions 16-18: Summary Completion',
            instructions='Complete the summary. Write NO MORE THAN TWO WORDS from the passage.',
            order=2,
            passage_text='Renewable energy includes several types. _____ (16) is growing fast and uses panels to convert sunlight. _____ (17) uses turbines to convert wind into power. _____ (18) has been used for over a century and uses water flow.'
        )

        summary_comp = [
            {'num': 16, 'text': 'Summary blank 16', 'answer': 'Solar power'},
            {'num': 17, 'text': 'Summary blank 17', 'answer': 'Wind energy'},
            {'num': 18, 'text': 'Summary blank 18', 'answer': 'Hydroelectric power'}
        ]

        for q in summary_comp:
            SummaryCompletionQuestion.objects.create(
                question_group=group6,
                question_number=q['num'],
                summary_text=q['text'],
                correct_answer=q['answer'],
                max_words=2,
                points=1
            )

        # Group 7: Note Completion
        group7 = QuestionGroup.objects.create(
            section=section2,
            question_type='note_completion',
            title='Questions 19-21: Note Completion',
            instructions='Complete the notes. Write NO MORE THAN TWO WORDS from the passage.',
            order=3,
            passage_text="""Notes on Renewable Energy:
- Solar: Uses _____ (19) to generate electricity
- Wind: _____ (20) wind farms are particularly effective
- Geothermal: Common in _____ (21) and New Zealand"""
        )

        note_comp = [
            {'num': 19, 'text': 'Note 19', 'answer': 'photovoltaic cells'},
            {'num': 20, 'text': 'Note 20', 'answer': 'Offshore'},
            {'num': 21, 'text': 'Note 21', 'answer': 'Iceland'}
        ]

        for q in note_comp:
            NoteCompletionQuestion.objects.create(
                question_group=group7,
                question_number=q['num'],
                note_text=q['text'],
                correct_answer=q['answer'],
                max_words=2,
                points=1
            )

        # Group 8: Table Completion
        group8 = QuestionGroup.objects.create(
            section=section2,
            question_type='table_completion',
            title='Questions 22-24: Table Completion',
            instructions='Complete the table. Write NO MORE THAN TWO WORDS from the passage.',
            order=4
        )

        table_comp = [
            {'num': 22, 'row': 'Solar', 'col': 'Technology', 'context': 'Uses photovoltaic cells', 'answer': 'photovoltaic cells'},
            {'num': 23, 'row': 'Wind', 'col': 'Equipment', 'context': 'Uses turbines', 'answer': 'turbines'},
            {'num': 24, 'row': 'Biomass', 'col': 'Source', 'context': 'Comes from organic materials', 'answer': 'organic materials'}
        ]

        for q in table_comp:
            TableCompletionQuestion.objects.create(
                question_group=group8,
                question_number=q['num'],
                row_header=q['row'],
                column_header=q['col'],
                cell_context=q['context'],
                correct_answer=q['answer'],
                max_words=2,
                points=1
            )

        # Group 9: Short Answer
        group9 = QuestionGroup.objects.create(
            section=section2,
            question_type='short_answer',
            title='Questions 25-27: Short Answer',
            instructions='Answer the questions. Write NO MORE THAN THREE WORDS from the passage.',
            order=5
        )

        short_answer = [
            {'num': 25, 'text': 'What has improved dramatically over the past decade?', 'answer': 'solar panel efficiency'},
            {'num': 26, 'text': 'What can large dams produce?', 'answer': 'enormous amounts power'},
            {'num': 27, 'text': 'What does biomass sustainability depend on?', 'answer': 'material sourcing'}
        ]

        for q in short_answer:
            ShortAnswerQuestion.objects.create(
                question_group=group9,
                question_number=q['num'],
                question_text=q['text'],
                correct_answer=q['answer'],
                max_words=3,
                points=1
            )

        # ==================== SECTION 3: Matching & Diagram Questions ====================
        section3 = Section.objects.create(
            exam=exam,
            title='Section 3: Matching & Diagram Questions',
            module='reading',
            order=3,
            passage_text="""THE WATER CYCLE

A. The water cycle, also known as the hydrological cycle, describes the continuous movement of water on, above, and below the surface of the Earth. This cycle is driven by solar energy and gravity.

B. Evaporation is the process by which water changes from liquid to gas. The sun heats water in oceans, lakes, and rivers, causing it to evaporate into the atmosphere. Plants also release water vapor through transpiration.

C. As water vapor rises into the atmosphere, it cools and condenses into tiny water droplets, forming clouds. This process is called condensation. The droplets combine to form larger drops.

D. When the water droplets in clouds become too heavy, they fall back to Earth as precipitation. This can be in the form of rain, snow, sleet, or hail, depending on temperature conditions.

E. Once precipitation reaches the ground, it follows several paths. Some water flows over the surface as runoff into rivers and streams. Some infiltrates into the soil, becoming groundwater. Plants absorb some water through their roots.

F. Groundwater slowly moves through underground aquifers and eventually returns to the surface through springs or wells. This underground water storage is crucial for maintaining river flow during dry periods.

G. The cycle then repeats as surface water evaporates again. This continuous process ensures that water is constantly recycled and distributed around the planet, supporting all forms of life.""",
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS(f'✓ Created section: {section3.title}'))

        # Group 10: Matching Headings
        group10 = QuestionGroup.objects.create(
            section=section3,
            question_type='matching_headings',
            title='Questions 28-34: Matching Headings',
            instructions='Match each paragraph (A-G) with the correct heading (i-ix).',
            order=1
        )

        headings = [
            ('i', 'Water returns to the atmosphere'),
            ('ii', 'Introduction to the water cycle'),
            ('iii', 'Water falls from the sky'),
            ('iv', 'Water becomes gas'),
            ('v', 'Water moves underground'),
            ('vi', 'Gas becomes liquid'),
            ('vii', 'Water takes different paths on land'),
            ('viii', 'The importance of oceans'),
            ('ix', 'The cycle continues'),
        ]

        for label, text in headings:
            HeadingOption.objects.create(
                question_group=group10,
                heading_label=label,
                heading_text=text,
                order=int(label[1:]) if label[1:].isdigit() else 0
            )

        heading_matches = [
            {'num': 28, 'para': 'A', 'heading': 'ii'},
            {'num': 29, 'para': 'B', 'heading': 'iv'},
            {'num': 30, 'para': 'C', 'heading': 'vi'},
            {'num': 31, 'para': 'D', 'heading': 'iii'},
            {'num': 32, 'para': 'E', 'heading': 'vii'},
            {'num': 33, 'para': 'F', 'heading': 'v'},
            {'num': 34, 'para': 'G', 'heading': 'ix'},
        ]

        for q in heading_matches:
            MatchingHeadingsQuestion.objects.create(
                question_group=group10,
                question_number=q['num'],
                paragraph_label=q['para'],
                correct_heading=q['heading'],
                points=1
            )

        # Group 11: Matching Information
        group11 = QuestionGroup.objects.create(
            section=section3,
            question_type='matching_information',
            title='Questions 35-37: Matching Information',
            instructions='Match each statement with the correct paragraph (A-G).',
            order=2
        )

        info_matches = [
            {'num': 35, 'info': 'Mentions the role of solar energy', 'para': 'A'},
            {'num': 36, 'info': 'Describes water storage underground', 'para': 'F'},
            {'num': 37, 'info': 'Explains different forms of precipitation', 'para': 'D'}
        ]

        for q in info_matches:
            MatchingInformationQuestion.objects.create(
                question_group=group11,
                question_number=q['num'],
                information_text=q['info'],
                correct_paragraph=q['para'],
                points=1
            )

        # Group 12: Matching Features
        group12 = QuestionGroup.objects.create(
            section=section3,
            question_type='matching_features',
            title='Questions 38-40: Matching Features',
            instructions='Match each process with its description (A-E).',
            order=3
        )

        features = [
            ('A', 'Evaporation'),
            ('B', 'Condensation'),
            ('C', 'Precipitation'),
            ('D', 'Infiltration'),
            ('E', 'Transpiration'),
        ]

        for label, text in features:
            FeatureOption.objects.create(
                question_group=group12,
                feature_label=label,
                feature_text=text,
                order=ord(label) - ord('A')
            )

        feature_matches = [
            {'num': 38, 'statement': 'Water changes from liquid to gas', 'feature': 'A'},
            {'num': 39, 'statement': 'Water vapor becomes liquid droplets', 'feature': 'B'},
            {'num': 40, 'statement': 'Water soaks into the soil', 'feature': 'D'}
        ]

        for q in feature_matches:
            MatchingFeaturesQuestion.objects.create(
                question_group=group12,
                question_number=q['num'],
                statement=q['statement'],
                correct_feature=q['feature'],
                points=1
            )

        # Group 13: Matching Sentence Endings
        group13 = QuestionGroup.objects.create(
            section=section3,
            question_type='matching_sentence_endings',
            title='Questions 41-43: Matching Sentence Endings',
            instructions='Complete each sentence with the correct ending (A-F).',
            order=4
        )

        endings = [
            ('A', 'into the atmosphere as water vapor.'),
            ('B', 'through underground aquifers.'),
            ('C', 'as rain, snow, sleet, or hail.'),
            ('D', 'by solar energy and gravity.'),
            ('E', 'through their roots from soil.'),
            ('F', 'into rivers and streams.'),
        ]

        for label, text in endings:
            SentenceEndingOption.objects.create(
                question_group=group13,
                ending_label=label,
                ending_text=text,
                order=ord(label) - ord('A')
            )

        sentence_matches = [
            {'num': 41, 'start': 'The water cycle is driven', 'ending': 'D'},
            {'num': 42, 'start': 'Water evaporates', 'ending': 'A'},
            {'num': 43, 'start': 'Precipitation falls', 'ending': 'C'}
        ]

        for q in sentence_matches:
            MatchingSentenceEndingsQuestion.objects.create(
                question_group=group13,
                question_number=q['num'],
                sentence_start=q['start'],
                correct_ending=q['ending'],
                points=1
            )

        # Group 14: Flowchart Completion
        group14 = QuestionGroup.objects.create(
            section=section3,
            question_type='flowchart_completion',
            title='Questions 44-46: Flowchart Completion',
            instructions='Complete the flowchart. Write NO MORE THAN TWO WORDS from the passage.',
            order=5
        )

        flowchart = [
            {'num': 44, 'pos': 'Box 1', 'context': 'Water heats and becomes vapor', 'answer': 'Evaporation'},
            {'num': 45, 'pos': 'Box 2', 'context': 'Vapor cools and forms clouds', 'answer': 'Condensation'},
            {'num': 46, 'pos': 'Box 3', 'context': 'Water falls from clouds', 'answer': 'Precipitation'}
        ]

        for q in flowchart:
            FlowchartCompletionQuestion.objects.create(
                question_group=group14,
                question_number=q['num'],
                box_position=q['pos'],
                box_context=q['context'],
                correct_answer=q['answer'],
                max_words=2,
                points=1
            )

        # Group 15: Diagram Labeling (without actual image for now)
        group15 = QuestionGroup.objects.create(
            section=section3,
            question_type='diagram_labeling',
            title='Questions 47-50: Diagram Labeling',
            instructions='Label the water cycle diagram below. Write NO MORE THAN TWO WORDS from the passage.',
            order=6
        )

        # Create a diagram question
        diagram_q = DiagramLabelingQuestion.objects.create(
            question_group=group15,
            question_number=47,
            instruction='Label the water cycle diagram (imagine a diagram showing the water cycle)',
            points=4
        )

        # Add labels for the diagram
        diagram_labels = [
            {'num': 1, 'answer': 'Evaporation'},
            {'num': 2, 'answer': 'Condensation'},
            {'num': 3, 'answer': 'Precipitation'},
            {'num': 4, 'answer': 'Runoff'}
        ]

        for label in diagram_labels:
            ImageLabel.objects.create(
                question=diagram_q,
                label_number=label['num'],
                correct_answer=label['answer']
            )

        # Summary
        self.stdout.write(self.style.SUCCESS('='*70))
        self.stdout.write(self.style.SUCCESS('✓ Successfully created complete exam with ALL question types!'))
        self.stdout.write(self.style.SUCCESS('='*70))
        self.stdout.write(self.style.SUCCESS(f'Exam ID: {exam.id}'))
        self.stdout.write(self.style.SUCCESS(f'Exam Title: {exam.title}'))
        self.stdout.write(self.style.SUCCESS(f'Total Sections: 3'))
        self.stdout.write(self.style.SUCCESS(f'Total Questions: 50'))
        self.stdout.write(self.style.SUCCESS('='*70))
        self.stdout.write(self.style.SUCCESS('Question Types Included:'))
        self.stdout.write(self.style.SUCCESS('  1. Multiple Choice (Single Answer)'))
        self.stdout.write(self.style.SUCCESS('  2. Multiple Choice (Multiple Answers)'))
        self.stdout.write(self.style.SUCCESS('  3. True/False/Not Given'))
        self.stdout.write(self.style.SUCCESS('  4. Yes/No/Not Given'))
        self.stdout.write(self.style.SUCCESS('  5. Sentence Completion'))
        self.stdout.write(self.style.SUCCESS('  6. Summary Completion'))
        self.stdout.write(self.style.SUCCESS('  7. Note Completion'))
        self.stdout.write(self.style.SUCCESS('  8. Table Completion'))
        self.stdout.write(self.style.SUCCESS('  9. Short Answer'))
        self.stdout.write(self.style.SUCCESS(' 10. Matching Headings'))
        self.stdout.write(self.style.SUCCESS(' 11. Matching Information'))
        self.stdout.write(self.style.SUCCESS(' 12. Matching Features'))
        self.stdout.write(self.style.SUCCESS(' 13. Matching Sentence Endings'))
        self.stdout.write(self.style.SUCCESS(' 14. Flowchart Completion'))
        self.stdout.write(self.style.SUCCESS(' 15. Diagram Labeling'))
        self.stdout.write(self.style.SUCCESS('='*70))
