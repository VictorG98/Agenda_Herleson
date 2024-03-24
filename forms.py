from django import forms
from .models import Contato, Grupo, Telefone, Email
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit

class EditarContatoForm(forms.Form):
    def __init__(self, *args, **kwargs):
        contato = Contato.objects.get(id=kwargs.pop('id'))
        self.contato = contato
        super(EditarContatoForm, self).__init__(*args, **kwargs)
        self.fields['nome_contato'] = forms.CharField(max_length=50, initial=contato.nome)
        grupos = Grupo.objects.all()
        grupos_contato = contato.grupos.all()
        for grupo in grupos:
            self.fields[f"g_{grupo.nome}"] = forms.BooleanField(required=False,
                                                                initial=grupo in grupos_contato,
                                                                label=f"{grupo.nome}")

        for i, tel in enumerate(contato.telefone_set.all()):
            self.fields[f"tel_{i}"] = forms.CharField(max_length=14,
                                                      label=f"Telefone {i+1}",
                                                      initial=contato.telefone_set.all()[i].numero)

        for i, email in enumerate(contato.email_set.all()):
            self.fields[f"email_{i}"] = forms.EmailField(max_length=255,
                                                      label=f"Email {i+1}",
                                                      initial=contato.email_set.all()[i].endereco)

    def clean_nome_contato(self):
        nome_contato = self.cleaned_data.get('nome_contato')
        nomes_contatos = []
        for contact in Contato.objects.all():
            nomes_contatos.append(contact.nome)
        nomes_contatos.remove(self.contato.nome)
        if nome_contato in nomes_contatos:
            raise forms.ValidationError("O nome escolhido já está sendo utilizado.")
        return nome_contato

class NovoGrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = ('nome', 'descricao')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('nome', css_class='form-control'),  # Adicione a classe form-control
            Field('descricao', css_class='form-control'),  # Adicione a classe form-control
            ButtonHolder(
                Submit('submit', 'Salvar', css_class='btn btn-primary')  # Adicione as classes CSS do Bootstrap
                )
            )

class NovoTelForm(forms.ModelForm):
    class Meta:
        model = Telefone
        fields = ('numero',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('numero', css_class='form-control'),  # Adicione a classe form-contro
            ButtonHolder(
                Submit('submit', 'Salvar', css_class='btn btn-primary')  # Adicione as classes CSS do Bootstrap
                )
            )

class NovoEmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ('endereco',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('endereco', css_class='form-control'),  # Adicione a classe form-control
            ButtonHolder(
                Submit('submit', 'Salvar', css_class='btn btn-primary')  # Adicione as classes CSS do Bootstrap
                )
            )
