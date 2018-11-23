from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from django.views import generic

# from django.template import loader

# importing the votes Models
from .models import Question, Choice

# Create your views here.

class IndexView(generic.ListView):
	template_name = 'voting/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		"""Return the last five published questions."""
		return Question.objects.order_by('-pub_date')[:8]

class DetailView(generic.DetailView):
	model = Question
	template_name = 'voting/detail.html'

class ResultsView(generic.DetailView):
	model = Question
	template_name = 'voting/results.html'

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		# Redisplay the question voting form.
		return render(
			request, 
			'voting/detail.html',
			{
				'question': question,
				'error_message': 'You did not select a choice!',
			}
		)
	else:
		# The F function stores the vote field on memory and then saved the object back to the database
		selected_choice.vote = F('vote') + 1
		#selected_choice.vote += 1
		selected_choice.save()

		return HttpResponseRedirect(reverse('voting:results', args=(question.id,)))





