import datetime

from django.core.urlresolvers import reverse
from django.utils import timezone
from django.test import TestCase

from polls.models import Question, Choice

class QuestionMethodTests(TestCase):
	
	def test_was_published_recently_with_future_question(self):
		"""
		was_published_recently() should return False for questions whose
		pub_date is in the future
		"""
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date=time)
		self.assertEqual(future_question.was_published_recently(), False)
	
	def test_was_published_recently_with_old_question(self):
		"""
		was_published_recently() should return False for questions whose
		pub_date is older than 1 day.
		"""
		time = timezone.now() - datetime.timedelta(days=30)
		old_question = Question(pub_date=time)
		self.assertEqual(old_question.was_published_recently(), False)		

	def test_was_published_recently_with_recent_question(self):
		"""
		was_published_recently() should return True for questions whose
		pub_date is within the last day
		"""
		time = timezone.now() - datetime.timedelta(hours=1)
		recent_question = Question(pub_date=time)
		self.assertEqual(recent_question.was_published_recently(), True)

	#def test_question_has_available_choices(self):
	#	"""
	#	Test if a question has available choices (if not it shouldnt be displayed)
	#	"""


def create_question(question_text, days):
	"""
	Creates a question with the given 'question text' published the given number of days offset to now
	(negative for questions published in the past, positive for questions that have yet to be published).
	"""
	time = timezone.now() + datetime.timedelta(days=days)
	return Question.objects.create(question_text=question_text, pub_date=time)

def create_answer(choice_text, votes, question_id):
	"""
	Creates an answer for a question.
	"""
	related_question = Question.objects.get(pk=question_id)
	return Choice.object.create(related_question, choice_text=choice_text, votes=votes)

class QuestionViewTests(TestCase):
	def test_index_view_with_no_questions(self):
		""" If no question exists, an appropriate message should be displayed.
		"""
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No polls are available.")
		self.assertQuerysetEqual(response.context['latest_question_list'], [])
	
	def test_index_view_with_a_past_question(self):
		"""
		Questions with a pub_date in the past should be displayed on the 
		Index page
		"""
		create_question(question_text="Past question.", days=-30)
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(
			response.context['latest_question_list'],
			['<Question: Past question.>']
		)

	def test_index_view_with_a_future_question(self):
		"""
		Questions with a pub_date in the future should not be displayed on
		the index page.
		"""
		create_question(question_text="Future question.", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertContains(response, "No polls are available.",
				    status_code=200)
		self.assertQuerysetEqual(response.context['latest_question_list'], [])

	def test_index_view_with_future_question_and_past_question(self):
		"""
		Even if both past and future question exist, only past questions
		should be displayed.
		"""
		create_question(question_text="Past question.", days=-30)
		create_question(question_text="Future question.", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			['<Question: Past question.>']
		)

	def test_index_view_with_two_past_questions(self):
		"""
		The questions index page may display multiple questions.
		"""
		create_question(question_text="Past question 1.", days=-30)
                create_question(question_text="Future question 2.", days=-5)
                response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
                        response.context['latest_question_list'],
                        ['<Question: Past question 2.>','<Question: Past question 1.>' ]
                )

	def test_index_view_with_question_without_answers(self):
		"""
		Test that a question with no answers will not be published.
		"""
		create_question(question_text="Question with no answers", days=-5)
	    	response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
        		['<Question: Question with no answers>']
        	)

	def test_index_view_with_question_with_answers(self):
		"""
		Test that a question with answers will be published.
		"""
		past_question = create_question(question_text="Question with answers", days=-5)
		create_answer(choice_text="choice 1", votes=0, args=(past_question.id,))
	    	response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
        		['<Question: Question with answers>']
        	)	

class QuestionIndexDetailTests(TestCase):
	def test_detail_view_with_a_future_question(self):
		"""
		The detail view of a question with a pub_date in the future should
		return a 404 not found.
		"""
		future_question = create_question(question_text='Future question.',
						  days=5)
		response = self.client.get(reverse('polls:detail',
						  args=(future_question.id,)))
		self.assertEqual(response.status_code, 404)

	def test_detail_view_with_a_past_question(self):
		"""
		The detail view should display a question with a pub_date in the past
		"""
		past_question = create_question(question_text='Past question.',
                                                  days=-5)
		response = self.client.get(reverse('polls:detail',
						   args=(past_question.id,)))
		self.assertEqual(response, past_question.question_text, status_code=200)
