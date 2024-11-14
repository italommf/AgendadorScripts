from django.contrib import admin
from .models import Scripts, Agendamento

class AgendamentoAdmin(admin.ModelAdmin):

    list_display = ('get_nome_script', 'get_responsavel_script', 'frequencia', 'tempo_repeticao', 'intervalo', 'hora_inicial', 'data_agendamento')
    list_filter = ('frequencia', 'tempo_repeticao', 'script__nome')
    search_fields = ('script__nome', 'script__caminho_script')
    fieldsets = (
        (None, {
            'fields': ('script', 'frequencia')
        }),
        ('Configurações de Repetição', {
            'fields': ('tempo_repeticao', 'intervalo', 'hora_inicial', 'hora_final'),
            'classes': ('collapse',),
            'description': 'Configure o intervalo de repetição para execuções frequentes.'
        }),
        ('Proxima Execução', {
            'fields': ('data_agendamento',),
            'description': 'Data e hora da próxima execução. Se vazio, o script executara imediatamente'
        }),
    )
    ordering = ('frequencia', 'hora_inicial')

    def get_nome_script(self, obj):
        return obj.script.nome
    get_nome_script.short_description = 'Nome do Script'

    def get_responsavel_script(self, obj):
        return obj.script.responsavel
    get_responsavel_script.short_description = 'Responsável'

admin.site.register(Agendamento, AgendamentoAdmin)

@admin.register(Scripts)
class ScriptsAdmin(admin.ModelAdmin):
    list_display = ('nome', 'responsavel', 'caminho_script')
