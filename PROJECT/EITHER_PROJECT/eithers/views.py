from django.shortcuts import render, redirect
from .models import Question, Answer
from django.db.models import Q, Count

# Create your views here.
def index(request):
    questions = Question.objects.order_by('-pk')
    # questions = Question.objects.prefetch_related('answer_set').order_by('-pk')
    context = {
        'questions': questions,
    }
    return render(request, 'eithers/index.html', context)

def new(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        issue_a = request.POST.get('issue_a')
        issue_b = request.POST.get('issue_b')
        image_a = request.FILES.get('image_a')
        image_b = request.FILES.get('image_b')

        question = Question(title=title, issue_a=issue_a, issue_b=issue_b, image_a=image_a, image_b=image_b)
        question.save()

        return redirect('eithers:index')
    else:
        return render(request, 'eithers/new.html')

def detail(request, question_pk):
    # 1
    # question = Question.objects.get(pk=question_pk)
    # question = Question.objects.prefetch_related('answer_set').get(pk=question_pk)
    # count_a = len(question.answer_set.filter(pick=0))
    # count_b = len(question.answer_set.filter(pick=1))
    
    # sum_ab = count_a + count_b

    # if sum_ab == 0:
    #     a_per = 0
    #     b_per = 0
    # else:
    #     a_per = round(count_a / sum_ab * 100, 2)
    #     b_per = round(count_b / sum_ab * 100, 2)
    
    # context = {
    #     'question': question, 
    #     'a_per': a_per, 
    #     'b_per': b_per,
    # }

    # 2
    # question = Question.objects.prefetch_related('answer_set').get(pk=question_pk)
    question = Question.objects.annotate(
                                sum_ab=Count('answer'),
                                count_a=Count('answer', filter=Q(answer__pick=0)),
                                count_b=Count('answer', filter=Q(answer__pick=1))
                            ).get(pk=question_pk)

    a_per = round(question.count_a / (question.sum_ab or 1) * 100, 2) or 0
    b_per = round(question.count_b / (question.sum_ab or 1) * 100, 2) or 0
    
    context = {
        'question': question, 
        'a_per': a_per, 
        'b_per': b_per,
    }

    return render(request, 'eithers/detail.html', context)

def answers_create(request, question_pk):
    question = Question.objects.get(pk=question_pk)
    pick = int(request.POST.get('pick'))
    comment = request.POST.get('comment')

    answer = Answer(question=question, pick=pick, comment=comment)
    answer.save()

    return redirect('eithers:detail', question_pk)

def answers_delete(request, question_pk, answer_pk):
    answer = Answer.objects.get(pk=answer_pk)
    if request.method == 'POST':
        answer.delete()
    return redirect('eithers:detail', question_pk)

def random(request):
    # 랜덤 정렬
    question = Question.objects.order_by('?')[0]
    count_a = len(question.answer_set.filter(pick=0))
    count_b = len(question.answer_set.filter(pick=1))
    sum_ab = count_a + count_b

    if sum_ab == 0:
        a_per = 0
        b_per = 0
    else:
        a_per = round(count_a / sum_ab * 100, 2)
        b_per = round(count_b / sum_ab * 100, 2)
    
    context = {
        'question': question, 
        'a_per': a_per, 
        'b_per': b_per,
    }

    return render(request, 'eithers/detail.html', context)
