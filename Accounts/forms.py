from django import forms

class MonthForm(forms.Form):
    months = [
        ('--------','--------'),
        ('January','January'),
                  ('February','February'),
                  ('March','March'),
                  ('April','April'),
                  ('May','May'),
                  ('June','June'),
                  ('July','July'),
                  ('August','August'),
                  ('September','September'),
                  ('October','October'),
                  ('November','November'),
                  ('December','December'),]
    month = forms.ChoiceField(choices=months)
