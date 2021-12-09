from django import forms

from challenges.models import Idea, Department
from challenges.forms import IdeaForm


class EnhancedIdeaForm(IdeaForm):
    """The form for idea submission with out binding with a challenge"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["department"].queryset = Department.objects.filter(
            is_approved=True
        )

    class Meta:
        model = Idea
        fields = ("title", "description", "department", "image", "is_pridar")
        labels = {
            "is_pridar": "Technology-related?",
            "department": "Department",
        }
