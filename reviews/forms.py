from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ["rating", "comment"]

        widgets = {
            "rating": forms.Select(choices=[
                (1, "1 Star"),
                (2, "2 Stars"),
                (3, "3 Stars"),
                (4, "4 Stars"),
                (5, "5 Stars"),
            ]),
            "comment": forms.Textarea(attrs={"rows": 4})
        }