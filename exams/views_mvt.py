from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import (
    Exam, Section, QuestionGroup, ExamLink,
    MultipleChoiceSingleQuestion, MultipleChoiceMultipleQuestion,
    TrueFalseNotGivenQuestion, YesNoNotGivenQuestion,
    SentenceCompletionQuestion, ShortAnswerQuestion,
    DiagramLabelingQuestion, SummaryCompletionQuestion,
)
from .forms import (
    ExamForm, SectionForm, QuestionGroupForm, ExamLinkForm,
    MultipleChoiceSingleForm, MultipleChoiceMultipleForm,
    TrueFalseNotGivenForm, YesNoNotGivenForm,
    SentenceCompletionForm, ShortAnswerForm,
    DiagramLabelingForm, SummaryCompletionForm,
)
from students.forms import StudentRegistrationForm
from students.models import Student


@login_required
def exam_list_view(request):
    """List all exams"""
    exams = Exam.objects.filter(organization=request.user).prefetch_related('sections')
    return render(request, 'exams/exam_list.html', {'exams': exams})


@login_required
def exam_create_view(request):
    """Create new exam"""
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.organization = request.user
            exam.save()
            messages.success(request, 'Imtihon muvaffaqiyatli yaratildi!')
            return redirect('exam_detail', pk=exam.pk)
    else:
        form = ExamForm()
    
    return render(request, 'exams/exam_form.html', {'form': form, 'title': 'Yangi imtihon'})


@login_required
def exam_detail_view(request, pk):
    """Exam detail view"""
    exam = get_object_or_404(Exam, pk=pk, organization=request.user)
    sections = exam.sections.all().order_by('order')
    links = exam.links.all()
    
    # Count total questions across all sections
    total_questions = 0
    for section in sections:
        for group in section.question_groups.all():
            # Count questions in each group based on question type
            if group.question_type == 'multiple_choice_single':
                total_questions += group.multiplechoicesinglequestion_set.count()
            elif group.question_type == 'multiple_choice_multiple':
                total_questions += group.multiplechoicemultiplequestion_set.count()
            elif group.question_type == 'true_false_ng':
                total_questions += group.truefalsenotgivenquestion_set.count()
            elif group.question_type == 'yes_no_ng':
                total_questions += group.yesnonotgivenquestion_set.count()
            elif group.question_type == 'sentence_completion':
                total_questions += group.sentencecompletionquestion_set.count()
            elif group.question_type == 'short_answer':
                total_questions += group.shortanswerquestion_set.count()
            elif group.question_type == 'diagram_labeling':
                total_questions += group.diagramlabelingquestion_set.count()
            elif group.question_type == 'summary_completion':
                total_questions += group.summarycompletionquestion_set.count()
    
    context = {
        'exam': exam,
        'sections': sections,
        'links': links,
        'total_questions': total_questions
    }
    
    return render(request, 'exams/exam_detail.html', context)


@login_required
def exam_edit_view(request, pk):
    """Edit exam"""
    exam = get_object_or_404(Exam, pk=pk, organization=request.user)
    
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            messages.success(request, 'Imtihon yangilandi!')
            return redirect('exam_detail', pk=exam.pk)
    else:
        form = ExamForm(instance=exam)
    
    return render(request, 'exams/exam_form.html', {'form': form, 'title': 'Imtihonni tahrirlash', 'exam': exam})


@login_required
def exam_delete_view(request, pk):
    """Delete exam"""
    exam = get_object_or_404(Exam, pk=pk, organization=request.user)
    
    if request.method == 'POST':
        exam.delete()
        messages.success(request, 'Imtihon o\'chirildi!')
        return redirect('exam_list')
    
    return render(request, 'exams/exam_confirm_delete.html', {'exam': exam})


@login_required
def section_create_view(request, exam_pk):
    """Create section for exam"""
    exam = get_object_or_404(Exam, pk=exam_pk, organization=request.user)
    
    if request.method == 'POST':
        form = SectionForm(request.POST, request.FILES)
        if form.is_valid():
            section = form.save(commit=False)
            section.exam = exam
            section.save()
            messages.success(request, 'Section muvaffaqiyatli yaratildi!')
            return redirect('exam_detail', pk=exam.pk)
    else:
        form = SectionForm()
    
    return render(request, 'exams/section_form.html', {
        'form': form,
        'exam': exam,
        'title': 'Yangi Section'
    })


@login_required
def question_group_create_view(request, section_pk):
    """Create question group for section"""
    section = get_object_or_404(Section, pk=section_pk, exam__organization=request.user)
    
    if request.method == 'POST':
        form = QuestionGroupForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.section = section
            group.save()
            messages.success(request, 'Savol guruhi yaratildi!')
            return redirect('question_group_detail', pk=group.pk)
    else:
        form = QuestionGroupForm()
    
    return render(request, 'exams/question_group_form.html', {
        'form': form,
        'section': section,
        'title': 'Yangi savol guruhi'
    })


@login_required
def question_group_detail_view(request, pk):
    """Question group detail - shows all questions in this group"""
    group = get_object_or_404(QuestionGroup, pk=pk, section__exam__organization=request.user)
    
    # Get questions based on type
    questions = []
    if group.question_type == 'multiple_choice_single':
        questions = group.multiplechoicesinglequestion_set.all()
    elif group.question_type == 'multiple_choice_multiple':
        questions = group.multiplechoicemultiplequestion_set.all()
    elif group.question_type == 'true_false_ng':
        questions = group.truefalsenotgivenquestion_set.all()
    elif group.question_type == 'yes_no_ng':
        questions = group.yesnonotgivenquestion_set.all()
    elif group.question_type == 'sentence_completion':
        questions = group.sentencecompletionquestion_set.all()
    elif group.question_type == 'short_answer':
        questions = group.shortanswerquestion_set.all()
    elif group.question_type == 'diagram_labeling':
        questions = group.diagramlabelingquestion_set.all()
    elif group.question_type == 'summary_completion':
        questions = group.summarycompletionquestion_set.all()
    
    context = {
        'group': group,
        'questions': questions,
        'section': group.section,
        'exam': group.section.exam
    }
    
    return render(request, 'exams/question_group_detail.html', context)


@login_required
def question_create_view(request, group_pk):
    """Add question to group - redirects to specific form based on question type"""
    group = get_object_or_404(QuestionGroup, pk=group_pk, section__exam__organization=request.user)
    
    # Redirect to specific question form based on group type
    type_url_map = {
        'multiple_choice_single': 'question_mcq_single_create',
        'multiple_choice_multiple': 'question_mcq_multiple_create',
        'true_false_ng': 'question_tfng_create',
        'yes_no_ng': 'question_ynng_create',
        'sentence_completion': 'question_sentence_create',
        'short_answer': 'question_short_answer_create',
        'diagram_labeling': 'question_diagram_create',
        'summary_completion': 'question_summary_create',
    }
    
    url_name = type_url_map.get(group.question_type)
    if url_name:
        return redirect(url_name, group_pk=group_pk)
    else:
        messages.error(request, 'Bu savol turi uchun forma hali tayyor emas')
        return redirect('question_group_detail', pk=group_pk)


# ==================== QUESTION TYPE VIEWS ====================

def _get_question_context(group):
    """Helper to build common context for question forms"""
    return {
        'group': group,
        'section': group.section,
        'exam': group.section.exam,
    }


def _get_next_question_number(group):
    """Helper to auto-calculate the next question number for a group"""
    question_type_map = {
        'multiple_choice_single': 'multiplechoicesinglequestion_set',
        'multiple_choice_multiple': 'multiplechoicemultiplequestion_set',
        'true_false_ng': 'truefalsenotgivenquestion_set',
        'yes_no_ng': 'yesnonotgivenquestion_set',
        'sentence_completion': 'sentencecompletionquestion_set',
        'short_answer': 'shortanswerquestion_set',
        'diagram_labeling': 'diagramlabelingquestion_set',
        'summary_completion': 'summarycompletionquestion_set',
    }
    related_name = question_type_map.get(group.question_type)
    if related_name:
        qs = getattr(group, related_name).all()
        if qs.exists():
            return qs.order_by('-question_number').first().question_number + 1
    return 1


@login_required
def question_mcq_single_create_view(request, group_pk):
    """Create MCQ single answer question"""
    group = get_object_or_404(QuestionGroup, pk=group_pk, section__exam__organization=request.user)
    
    if request.method == 'POST':
        form = MultipleChoiceSingleForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.question_group = group
            question.save()
            messages.success(request, f'Savol #{question.question_number} muvaffaqiyatli qo\'shildi!')
            if 'save_and_add' in request.POST:
                return redirect('question_mcq_single_create', group_pk=group.pk)
            return redirect('question_group_detail', pk=group.pk)
    else:
        initial = {'question_number': _get_next_question_number(group)}
        form = MultipleChoiceSingleForm(initial=initial)
    
    context = _get_question_context(group)
    context.update({
        'form': form,
        'title': 'Multiple Choice (Single Answer) savol qo\'shish',
        'question_type_display': 'Multiple Choice (Single Answer)',
    })
    return render(request, 'exams/question_type_form.html', context)


@login_required
def question_mcq_multiple_create_view(request, group_pk):
    """Create MCQ multiple answers question"""
    group = get_object_or_404(QuestionGroup, pk=group_pk, section__exam__organization=request.user)
    
    if request.method == 'POST':
        form = MultipleChoiceMultipleForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.question_group = group
            question.save()
            messages.success(request, f'Savol #{question.question_number} muvaffaqiyatli qo\'shildi!')
            if 'save_and_add' in request.POST:
                return redirect('question_mcq_multiple_create', group_pk=group.pk)
            return redirect('question_group_detail', pk=group.pk)
    else:
        initial = {'question_number': _get_next_question_number(group)}
        form = MultipleChoiceMultipleForm(initial=initial)
    
    context = _get_question_context(group)
    context.update({
        'form': form,
        'title': 'Multiple Choice (Multiple Answers) savol qo\'shish',
        'question_type_display': 'Multiple Choice (Multiple Answers)',
    })
    return render(request, 'exams/question_type_form.html', context)


@login_required
def question_tfng_create_view(request, group_pk):
    """Create True/False/Not Given question"""
    group = get_object_or_404(QuestionGroup, pk=group_pk, section__exam__organization=request.user)
    
    if request.method == 'POST':
        form = TrueFalseNotGivenForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.question_group = group
            question.save()
            messages.success(request, f'Savol #{question.question_number} muvaffaqiyatli qo\'shildi!')
            if 'save_and_add' in request.POST:
                return redirect('question_tfng_create', group_pk=group.pk)
            return redirect('question_group_detail', pk=group.pk)
    else:
        initial = {'question_number': _get_next_question_number(group)}
        form = TrueFalseNotGivenForm(initial=initial)
    
    context = _get_question_context(group)
    context.update({
        'form': form,
        'title': 'True/False/Not Given savol qo\'shish',
        'question_type_display': 'True / False / Not Given',
    })
    return render(request, 'exams/question_type_form.html', context)


@login_required
def question_ynng_create_view(request, group_pk):
    """Create Yes/No/Not Given question"""
    group = get_object_or_404(QuestionGroup, pk=group_pk, section__exam__organization=request.user)
    
    if request.method == 'POST':
        form = YesNoNotGivenForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.question_group = group
            question.save()
            messages.success(request, f'Savol #{question.question_number} muvaffaqiyatli qo\'shildi!')
            if 'save_and_add' in request.POST:
                return redirect('question_ynng_create', group_pk=group.pk)
            return redirect('question_group_detail', pk=group.pk)
    else:
        initial = {'question_number': _get_next_question_number(group)}
        form = YesNoNotGivenForm(initial=initial)
    
    context = _get_question_context(group)
    context.update({
        'form': form,
        'title': 'Yes/No/Not Given savol qo\'shish',
        'question_type_display': 'Yes / No / Not Given',
    })
    return render(request, 'exams/question_type_form.html', context)


@login_required
def question_sentence_create_view(request, group_pk):
    """Create Sentence Completion question"""
    group = get_object_or_404(QuestionGroup, pk=group_pk, section__exam__organization=request.user)
    
    if request.method == 'POST':
        form = SentenceCompletionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.question_group = group
            question.save()
            messages.success(request, f'Savol #{question.question_number} muvaffaqiyatli qo\'shildi!')
            if 'save_and_add' in request.POST:
                return redirect('question_sentence_create', group_pk=group.pk)
            return redirect('question_group_detail', pk=group.pk)
    else:
        initial = {'question_number': _get_next_question_number(group)}
        form = SentenceCompletionForm(initial=initial)
    
    context = _get_question_context(group)
    context.update({
        'form': form,
        'title': 'Sentence Completion savol qo\'shish',
        'question_type_display': 'Sentence Completion',
    })
    return render(request, 'exams/question_type_form.html', context)


@login_required
def question_short_answer_create_view(request, group_pk):
    """Create Short Answer question"""
    group = get_object_or_404(QuestionGroup, pk=group_pk, section__exam__organization=request.user)
    
    if request.method == 'POST':
        form = ShortAnswerForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.question_group = group
            question.save()
            messages.success(request, f'Savol #{question.question_number} muvaffaqiyatli qo\'shildi!')
            if 'save_and_add' in request.POST:
                return redirect('question_short_answer_create', group_pk=group.pk)
            return redirect('question_group_detail', pk=group.pk)
    else:
        initial = {'question_number': _get_next_question_number(group)}
        form = ShortAnswerForm(initial=initial)
    
    context = _get_question_context(group)
    context.update({
        'form': form,
        'title': 'Short Answer savol qo\'shish',
        'question_type_display': 'Short Answer',
    })
    return render(request, 'exams/question_type_form.html', context)


@login_required
def question_diagram_create_view(request, group_pk):
    """Create Diagram Labeling question"""
    group = get_object_or_404(QuestionGroup, pk=group_pk, section__exam__organization=request.user)
    
    if request.method == 'POST':
        form = DiagramLabelingForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.question_group = group
            question.save()
            messages.success(request, f'Savol #{question.question_number} muvaffaqiyatli qo\'shildi!')
            if 'save_and_add' in request.POST:
                return redirect('question_diagram_create', group_pk=group.pk)
            return redirect('question_group_detail', pk=group.pk)
    else:
        initial = {'question_number': _get_next_question_number(group)}
        form = DiagramLabelingForm(initial=initial)
    
    context = _get_question_context(group)
    context.update({
        'form': form,
        'title': 'Diagram Labeling savol qo\'shish',
        'question_type_display': 'Diagram Labeling',
    })
    return render(request, 'exams/question_type_form.html', context)


@login_required
def question_summary_create_view(request, group_pk):
    """Create Summary Completion question"""
    group = get_object_or_404(QuestionGroup, pk=group_pk, section__exam__organization=request.user)
    
    if request.method == 'POST':
        form = SummaryCompletionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.question_group = group
            question.save()
            messages.success(request, f'Savol #{question.question_number} muvaffaqiyatli qo\'shildi!')
            if 'save_and_add' in request.POST:
                return redirect('question_summary_create', group_pk=group.pk)
            return redirect('question_group_detail', pk=group.pk)
    else:
        initial = {'question_number': _get_next_question_number(group)}
        form = SummaryCompletionForm(initial=initial)
    
    context = _get_question_context(group)
    context.update({
        'form': form,
        'title': 'Summary Completion savol qo\'shish',
        'question_type_display': 'Summary Completion',
    })
    return render(request, 'exams/question_type_form.html', context)


@login_required
def question_delete_view(request, group_pk, pk):
    """Delete question from any question type"""
    group = get_object_or_404(QuestionGroup, pk=group_pk, section__exam__organization=request.user)
    
    # Find and delete the question from the correct model
    question = None
    model_map = {
        'multiple_choice_single': MultipleChoiceSingleQuestion,
        'multiple_choice_multiple': MultipleChoiceMultipleQuestion,
        'true_false_ng': TrueFalseNotGivenQuestion,
        'yes_no_ng': YesNoNotGivenQuestion,
        'sentence_completion': SentenceCompletionQuestion,
        'short_answer': ShortAnswerQuestion,
        'diagram_labeling': DiagramLabelingQuestion,
        'summary_completion': SummaryCompletionQuestion,
    }
    
    model_class = model_map.get(group.question_type)
    if model_class:
        question = get_object_or_404(model_class, pk=pk, question_group=group)
    
    if request.method == 'POST' and question:
        q_num = question.question_number
        question.delete()
        messages.success(request, f'Savol #{q_num} o\'chirildi!')
        return redirect('question_group_detail', pk=group.pk)
    
    return render(request, 'exams/question_confirm_delete.html', {
        'question': question,
        'group': group,
        'exam': group.section.exam,
    })


@login_required
def generate_link_view(request, exam_pk):
    """Generate exam link"""
    exam = get_object_or_404(Exam, pk=exam_pk, organization=request.user)
    
    if request.method == 'POST':
        form = ExamLinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.exam = exam
            expires_in_days = form.cleaned_data.get('expires_in_days')
            if expires_in_days:
                link.expires_at = timezone.now() + timedelta(days=expires_in_days)
            link.save()
            messages.success(request, 'Link yaratildi!')
            return redirect('exam_detail', pk=exam.pk)
    else:
        form = ExamLinkForm()
    
    return render(request, 'exams/link_form.html', {'form': form, 'exam': exam})


@login_required
def delete_link_view(request, pk):
    """Delete exam link"""
    link = get_object_or_404(ExamLink, pk=pk)
    exam = link.exam
    
    # Check permission
    if exam.organization != request.user:
        messages.error(request, 'Ruxsat yo\'q!')
        return redirect('exam_list')
    
    link.delete()
    messages.success(request, 'Link o\'chirildi!')
    return redirect('exam_detail', pk=exam.pk)


def exam_start_view(request, token):
    """Public exam start view"""
    exam_link = get_object_or_404(ExamLink, unique_token=token)
    
    if not exam_link.is_valid():
        return render(request, 'exams/link_expired.html', {'exam_link': exam_link})
    
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, organization=exam_link.exam.organization)
        if form.is_valid():
            student = form.save()
            exam_link.use_count += 1
            exam_link.save()
            return redirect('exam_take', token=token, student_id=student.id)
    else:
        form = StudentRegistrationForm(organization=exam_link.exam.organization)
    
    return render(request, 'exams/exam_start.html', {
        'form': form,
        'exam': exam_link.exam,
        'exam_link': exam_link
    })


def exam_take_view(request, token, student_id):
    """Exam taking view"""
    exam_link = get_object_or_404(ExamLink, unique_token=token)
    student = get_object_or_404(Student, pk=student_id)
    exam = exam_link.exam
    sections = exam.sections.all().order_by('order')
    
    # Build structured data for sections with their questions
    sections_data = []
    all_questions = []
    question_counter = 0
    
    for section in sections:
        section_info = {
            'id': section.id,
            'title': section.title,
            'module': section.module,
            'module_display': section.get_module_display(),
            'passage_text': section.passage_text,
            'audio_file': section.audio_file if section.audio_file else None,
            'audio_url': section.audio_url,
            'image': section.image if section.image else None,
            'groups': [],
        }
        
        for group in section.question_groups.all().order_by('order'):
            group_info = {
                'id': group.id,
                'title': group.title,
                'instructions': group.instructions,
                'question_type': group.question_type,
                'question_type_display': group.get_question_type_display(),
                'passage_text': group.passage_text,
                'image': group.image if group.image else None,
                'questions': [],
            }
            
            # Get questions based on type
            raw_questions = []
            if group.question_type == 'multiple_choice_single':
                raw_questions = group.multiplechoicesinglequestion_set.all().order_by('question_number')
            elif group.question_type == 'multiple_choice_multiple':
                raw_questions = group.multiplechoicemultiplequestion_set.all().order_by('question_number')
            elif group.question_type == 'true_false_ng':
                raw_questions = group.truefalsenotgivenquestion_set.all().order_by('question_number')
            elif group.question_type == 'yes_no_ng':
                raw_questions = group.yesnonotgivenquestion_set.all().order_by('question_number')
            elif group.question_type == 'sentence_completion':
                raw_questions = group.sentencecompletionquestion_set.all().order_by('question_number')
            elif group.question_type == 'short_answer':
                raw_questions = group.shortanswerquestion_set.all().order_by('question_number')
            elif group.question_type == 'diagram_labeling':
                raw_questions = group.diagramlabelingquestion_set.all().order_by('question_number')
            elif group.question_type == 'summary_completion':
                raw_questions = group.summarycompletionquestion_set.all().order_by('question_number')
            
            for q in raw_questions:
                question_counter += 1
                q_data = {
                    'id': q.id,
                    'counter': question_counter,
                    'question_number': q.question_number,
                    'question_type': group.question_type,
                    'points': q.points,
                    'group_id': group.id,
                }
                
                # Normalize question text and options based on type
                if group.question_type in ('multiple_choice_single', 'multiple_choice_multiple'):
                    q_data['text'] = q.question_text
                    q_data['options'] = {
                        'A': q.option_a,
                        'B': q.option_b,
                        'C': q.option_c,
                        'D': q.option_d,
                    }
                    if group.question_type == 'multiple_choice_multiple':
                        if hasattr(q, 'option_e') and q.option_e:
                            q_data['options']['E'] = q.option_e
                        if hasattr(q, 'option_f') and q.option_f:
                            q_data['options']['F'] = q.option_f
                elif group.question_type in ('true_false_ng', 'yes_no_ng'):
                    q_data['text'] = q.statement
                    if group.question_type == 'true_false_ng':
                        q_data['options'] = {'TRUE': 'True', 'FALSE': 'False', 'NOT GIVEN': 'Not Given'}
                    else:
                        q_data['options'] = {'YES': 'Yes', 'NO': 'No', 'NOT GIVEN': 'Not Given'}
                elif group.question_type == 'sentence_completion':
                    q_data['text'] = q.sentence_text
                    q_data['max_words'] = q.max_words
                elif group.question_type == 'short_answer':
                    q_data['text'] = q.question_text
                    q_data['max_words'] = q.max_words
                elif group.question_type == 'summary_completion':
                    q_data['text'] = q.summary_text
                    q_data['max_words'] = q.max_words
                elif group.question_type == 'diagram_labeling':
                    q_data['text'] = f"Label position: {q.label_position}"
                    if q.diagram_image:
                        q_data['diagram_image'] = q.diagram_image.url
                
                group_info['questions'].append(q_data)
                all_questions.append(q_data)
            
            section_info['groups'].append(group_info)
        
        sections_data.append(section_info)
    
    context = {
        'exam': exam,
        'sections_data': sections_data,
        'all_questions': all_questions,
        'total_questions': question_counter,
        'student': student,
        'exam_link': exam_link,
        'duration_seconds': exam.duration * 60
    }
    
    return render(request, 'exams/exam_take.html', context)
