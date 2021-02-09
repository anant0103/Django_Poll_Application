from django.test import TestCase

# Create your tests here.
from django.urls import reverse
import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time=timezone.now()+datetime.timedelta(days=30)
        future_question=Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(),False)

    def test_was_published_recently_with_old_question(self):
        time=timezone.now()-datetime.timedelta(days=1,seconds=1)
        past_question=Question(pub_date=time)
        self.assertIs(past_question.was_published_recently(),False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        responce=self.client.get(reverse('polls:index'))
        self.assertEqual(responce.status_code,200)
        self.assertContains(responce,"No polls are available.")
        self.assertQuerysetEqual(responce.context['latest_question_list'],[])

    def test_past_question(self):
        create_question(question_text="Past Question",days=-30)
        responce=self.client.get(reverse('polls:index'))
        self.assertEqual(responce.status_code,200)
        self.assertQuerysetEqual(responce.context['latest_question_list'],['<Question: Past Question>'])

    def test_future_question(self):
        create_question(question_text="Future Question",days=30)
        responce=self.client.get(reverse('polls:index'))
        self.assertEqual(responce.status_code,200)
        self.assertQuerysetEqual(responce.context['latest_question_list'],[])

    def test_future_question_and_past_question(self):
        create_question(question_text="Past Question",days=-30)
        create_question(question_text="Future Question",days=30)
        responce=self.client.get(reverse('polls:index'))
        self.assertEqual(responce.status_code,200)
        self.assertQuerysetEqual(responce.context['latest_question_list'],['<Question: Past Question>'])

    def test_two_past_questions(self):
        create_question(question_text="Past Question1",days=-30)
        create_question(question_text="Past Question2", days=-20)
        responce=self.client.get(reverse('polls:index'))
        self.assertEqual(responce.status_code,200)
        self.assertQuerysetEqual(responce.context['latest_question_list'],['<Question: Past Question2>','<Question: Past Question1>'])

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        future_question=create_question(question_text='Future question',days=5)
        url=reverse('polls:detail',args=(future_question.id,))
        responce=self.client.get(url)
        self.assertEqual(responce.status_code,404)

    def test_past_question(self):
        past_question = create_question(question_text='Past question', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        responce = self.client.get(url)
        self.assertContains(responce, past_question.question_text)