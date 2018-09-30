from django import forms
from dashboard.tasks import some_proccess


class CalculatorForm(forms.Form):
    x_value = forms.CharField(label="X Value", widget=forms.TextInput(attrs={
                                                        'size': 5,
                                                        'maxlength': 5})
                              )
    supercaptcha = forms.CharField(widget=forms.HiddenInput(), required=False)

    def calc(self, x):
        # a simple anti spam filter
        if self.cleaned_data['supercaptcha']:
            return False
        return some_proccess.delay(x)
