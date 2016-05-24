from django import forms


class RecipeSearchForm(forms.Form):
    query = forms.CharField(
        max_length=128,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "cocktails-search-text-field",
            "placeholder": "Поиск"})
    )

    is_long = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"id": "long-checkbox"})
    )

    is_shot = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"id": "shot-checkbox"})
    )

    is_strong = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"id": "strong-checkbox"})
    )

    is_non_alcoholic = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"id": "non-alcoholic-checkbox"})
    )
