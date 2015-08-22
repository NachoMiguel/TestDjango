from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice

# Create your views here.


class IndexView(generic.ListView):
    template_name = 'wiki/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions. (not included those set to be published in the future)"""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    #__lte_ less then or equal, en este case : menor o igual al dia de hoy


class DetailView(generic.DetailView):
    model = Question
    template_name = 'wiki/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'wiki/results.html'


def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'wiki/detail.html', {
            'question': p,
            'error_message': "You didnt select a choice.", })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('wiki:results', args=(p.id,)))



################# Primera parte del tutorial las vistas sin usar generic views #####################
#
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'wiki/index.html', context)


# def detail(request, question_id):
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     # return render(request, 'wiki/detail.html', {'question': question})
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'wiki/detail.html', {'question': question})


# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "wiki/results.html", {'question': question})



