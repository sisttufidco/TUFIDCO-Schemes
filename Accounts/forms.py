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
    scheme = [ 
        ("--------","--------"),
        ('KNMT', 'KNMT'),
        ('Singara Chennai 2.0','Singara Chennai 2.0')
    ]
    month = forms.ChoiceField(choices=months)
    Scheme = forms.ChoiceField(choices=scheme)
    

