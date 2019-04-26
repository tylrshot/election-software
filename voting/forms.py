from django import forms
from .models import Poll, Question, Choice, User

'''

class PollForm(forms.Form):
    def __init__(self, data, questions, *args, **kwargs):
        self.questions = questions
        for question in questions:
            field_name = "question_%d" % question.pk
            choices = []
            for choice in question.choice_set().all():
                choices.append((choice.pk, choice.choice,))
            ## May need to pass some initial data, etc:
            field = forms.ChoiceField(label=question.question, required=True, 
                                      choices=choices, widget=forms.RadioSelect)
        return super(QuizForm, self).__init__(data, *args, **kwargs)
    def save(self):
        ## Loop back through the question/answer fields and manually
        ## update the Attempt instance before returning it.
        
class NewPollForm(forms.Form):
    def __init__(self, data, questions, *args, **kwargs):
        self.questions = questions
        for Question in questions:
            choices = Choice.objects.filter(question=Question)
            thisQuestion = forms.MulitpleChoiceField(choices=choices)
            
            '''
                
