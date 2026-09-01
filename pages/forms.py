from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        label="Ваше ім'я",
        min_length=2,
        max_length=100,
        )
    email = forms.EmailField(label="Ваш email")
    repeat_email = forms.EmailField(label="Повторіть ваш email")
    message = forms.CharField(label="Ваше повідомлення", widget=forms.Textarea, required=False)
    agree = forms.BooleanField(label="Я згоден з умовами")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if email.endswith(".ru"):
            raise forms.ValidationError("Російські домени заборонені.")
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("email") != cleaned_data.get("repeat_email"):
            #raise forms.ValidationError("Email та повторний email повині співпадати.")
            self.add_error("repeat_email", "Email та повторний email повинні співпадати.")
        return cleaned_data