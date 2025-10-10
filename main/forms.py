# William Keilsohn
# October 9 2025

# Import Packages
from django import forms
from django.forms.widgets import Select
from .study.study import pre_process_choices

class TestForm(forms.Form):
    answers = forms.ChoiceField(
        label="Select a button",
        choices=[
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4)
        ],
        widget=forms.RadioSelect
    )

class CustomHanziAnswers(Select):

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)
        return option
        
class AnswerForm(forms.Form):
    answers = forms.ChoiceField(label="What is the meaning of this character?")

    def __init__(self, ans_ls=None, *args, **kwargs):
        field_choices = pre_process_choices(ans_ls)
        super().__init__(*args, **kwargs)
        self.fields['answers'] = forms.ChoiceField(choices=field_choices, widget=CustomHanziAnswers)

