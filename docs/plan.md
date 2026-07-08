# Engineering Doc Organizer — Plano do Projeto

> **Autor:** Raphael Prates  
> **Empresa:** OTAMERICA — Vila Velha / ES  
> **Objetivo de carreira:** AI Engineering  
> **Stack:** Python, Streamlit, SQLite, Tesseract, Anthropic API  
> **Repositório:** github.com/raphael-prates/engineering-doc-organizer

---

## Contexto do Projeto

Raphael é engenheiro civil na OTAMERICA e está aprendendo Python para seguir carreira em AI Engineering. Concluiu o CS50P e está construindo este projeto como primeiro projeto real em Python, com tutoria passo a passo — escrevendo cada linha de código para entender profundamente o que está sendo feito.

O projeto nasceu de uma necessidade real: organizar documentos de engenharia (plantas, memoriais, checklists) que chegam em pastas bagunçadas, sem padrão de nomenclatura, sem estrutura de diretórios consistente. A solução é uma aplicação desktop que lê o padrão de nomenclatura da empresa, cria a estrutura de pastas, classifica os arquivos e os distribui corretamente — com segurança e auditoria.

---

## Objetivo do Produto

Aplicação desktop para:
- Organizar documentos de engenharia em estrutura de pastas padronizada
- Renomear arquivos conforme norma da empresa (ex: OTTS-016)
- Detectar revisões e mover obsoletos automaticamente
- Gerar lista de documentos versionada ao final de cada operação
- Funcionar 100% local — sem exposição de dados sensíveis de projeto

---

## Stack Técnica

| Componente | Tecnologia | Finalidade |
|---|---|---|
| Interface | Streamlit | UI rápida sem HTML/CSS |
| Lógica core | Python stdlib | Scanner, Classifier, Renamer |
| OCR local | Tesseract + PIL | Leitura de carimbo em PDF/DWG |
| IA padrão | Anthropic Haiku 4.5 | Extrair padrão de nomenclatura |
| Banco de dados | SQLite | Histórico e logs (fase futura) |
| Exportação | openpyxl | Lista de documentos .xlsx |

---

## Decisões de Produto

### Privacidade e Segurança

- **Nomes de arquivo e metadados:** nunca saem da máquina
- **Conteúdo interno de arquivos** (plantas, memoriais): processado localmente via Tesseract
- **Padrão de nomenclatura:** enviado ao Haiku com aviso explícito ao usuário
- **Modo A (API Haiku):** usuário cola só o trecho do padrão — sem dado sensível de projeto
- **Modo B (manual):** usuário digita o padrão diretamente — zero dado externo
- **Modo C (Ollama local):** modelo open source, 100% offline — para ambientes de alta restrição

### Cleanup
Removido do escopo — operação feita pasta a pasta, de forma controlada. Mais seguro para o usuário final.

### Internacionalização
Interface desenvolvida em inglês. Tradução via sistema de locales (gettext ou i18n com JSON) planejada para Sprint 12.

---

## Fluxo do Produto

### FASE 1 — Configuração (feita uma vez por projeto)

**Etapa 1 — Padrão de nomenclatura**
Usuário cola trecho do procedimento da empresa. Haiku 4.5 interpreta e extrai o padrão. Suporta múltiplos padrões (ex: Documentação Técnica, Controle de Documentos). Usuário confirma antes de salvar.

**Etapa 2 — Estrutura de diretórios**
IA sugere estrutura de pastas baseada no padrão lido. Usuário visualiza em cascata e edita livremente. Ex: `Projeto / CIV / Emissões Finais / Obsoletos e Revisões`.

**Etapa 3 — Criação das pastas**
Programa cria a estrutura confirmada no disco. Pastas ficam vazias — nenhum arquivo é movido ainda.

---

### FASE 2 — Operação (repetida por emissão / ciclo de revisão)

**Etapa 4 — Destino e origem**
Usuário escolhe pasta de destino (ex: Emissões Finais) e pasta de origem com os arquivos novos.

**Etapa 5 — Scan e classificação**
Scanner percorre a origem. Classifier identifica disciplina, tipo, área, revisão. Stamp reader (Tesseract local) atua nos arquivos sem revisão no nome — sem enviar dados para fora da máquina.

**Etapa 6 — Gestão de revisões**
App compara arquivos novos com existentes no destino pelo código base. Se detectar revisão: pergunta onde mover o arquivo antigo (Obsoletos). Pergunta se quer fixar esse diretório como padrão para os próximos.

**Etapa 7 — Revisão e aprovação**
Tabela editável: arquivo → nome sugerido → pasta de destino → ação (mover / renomear / arquivar anterior / ignorar). Usuário aprova antes de qualquer movimentação.

**Etapa 8 — Execução segura**
Default: cria cópia do projeto (Projeto-org) antes de executar. Exibe alerta de risco para edição direta. Gera log completo da operação.

**Etapa 9 — Lista de documentos versionada**
Gerada automaticamente após cada operação. Lista todos os arquivos da pasta pai: código, título, disciplina, revisão, data, caminho. Salva como `Lista_Docs_v01.xlsx`, `v02`... Versões antigas mantidas para registro histórico.

---

## Arquitetura de Módulos

```
engineering-doc-organizer/
├── app.py                          # Entry point Streamlit
├── config/
│   ├── settings.py                 # Constantes globais
│   └── standards/                  # JSONs dos padrões salvos
│       └── otts016.json
├── core/
│   ├── models.py                   # EngineeringFile, Project
│   ├── scanner.py                  # Scan recursivo de pastas
│   ├── classifier.py               # Classificação por regex
│   ├── standard_extractor.py       # Extração de padrão de nomenclatura
│   ├── suggestion_engine.py        # (pendente Sprint 9)
│   ├── renamer.py                  # (pendente Sprint 10)
│   └── stamp_reader.py             # (pendente Sprint 8)
├── ui/
│   └── pages/
│       ├── config_page.py          # Padrão de nomenclatura ✓
│       ├── folder_page.py          # Estrutura de diretórios
│       ├── scan_page.py            # Scan + classificação
│       ├── review_page.py          # Revisão e aprovação
│       └── apply_page.py           # Execução e log
└── data/
    └── exports/                    # CSVs de scan e classificação
```

---

## EAP — Estrutura Analítica do Projeto

| Sprint | Status | Entrega |
|---|---|---|
| Sprint 1 | ✅ Concluído | Scanner — scan recursivo, detect_pattern, export CSV |
| Sprint 2 | ✅ Concluído | Classifier — mapeamento por regex, validação OTTS-016, orphan DWG |
| Sprint 3 | ✅ Concluído | app.py + estrutura de páginas Streamlit com stubs |
| Sprint 4 | ✅ Concluído | config_page + standard_extractor — múltiplos padrões, save/delete/clear |
| Sprint 5 | 🔨 Próximo | Estrutura de diretórios — UI em cascata, edição de template, folder_page |
| Sprint 6 | ⏳ Pendente | Criação de pastas no disco — pathlib, integração com template |
| Sprint 7 | ⏳ Pendente | Scan page + seleção de destino e origem |
| Sprint 8 | ⏳ Pendente | Stamp reader — Tesseract local, leitura de carimbo PDF/DWG |
| Sprint 9 | ⏳ Pendente | Gestão de revisões — detecção, mover obsoletos, padrão de destino |
| Sprint 10 | ⏳ Pendente | Review page + execução segura — tabela editável, log, cópia |
| Sprint 11 | ⏳ Pendente | Lista de documentos versionada — openpyxl, v01/v02... |
| Sprint 12 | ⏳ Pendente | Polimento e testes — UX, i18n, edge cases, projeto real OTAMERICA |

---

## Contexto de Sessões — O que foi feito

### Sprints 1 e 2
- `models.py`: classes `EngineeringFile` e `Project`
- `scanner.py`: scan recursivo com `os.walk`, `detect_pattern`, `check_path_length`, `export_csv`
- `classifier.py`: classifica por regex OTTS-016, valida disciplina/tipo/área, detecta orphan DWGs, `validate_move` com `ValueError`
- `config/settings.py`: constantes `TRASH_PREFIXES`, `OTTS016_PATTERN`, `MAX_PATH_LENGTH`
- `config/standards/otts016.json`: códigos válidos de disciplina, tipo de documento e área

### Sprint 3
- `app.py`: entry point com `st.set_page_config`, `st.title`, sidebar com `st.radio`, roteamento para páginas
- `ui/pages/`: stubs criados manualmente com função `render()` para cada página

### Sprint 4
- `core/standard_extractor.py`: 
  - `receive_input(input_data)` — aceita string ou bytes, retorna string UTF-8
  - `extract_pattern(text)` — usa `re.findall` com regex genérico, retorna lista de padrões
  - `save_standard(pattern, name)` — salva JSON em `config/standards/{name}.json`
  - `list_standards()` — lista nomes dos JSONs salvos
  - `load_standard(name)` — carrega JSON de um padrão
  - `delete_standard(name)` — remove arquivo JSON
- `ui/pages/config_page.py`:
  - Seção "Saved Standards" com dropdown e botão Delete
  - Seção "File Pattern Config" com text_area, file_uploader, Search e Clear
  - Gestão de session_state para inputs dinâmicos (text_key, upload_key)
  - Validações: nome obrigatório, nome único antes de salvar
  - Auto-seleção do padrão recém-salvo no dropdown

---

## Próximos Passos — Sprint 5

**Objetivo:** implementar `folder_page.py` — UI em cascata para o usuário definir a estrutura de diretórios do projeto.

**O que construir:**
1. Input para o usuário digitar o nome do projeto (pasta raiz)
2. UI interativa para adicionar subpastas em cascata
3. Preview visual da árvore de diretórios
4. Salvar o template em JSON (`config/folder_templates/{name}.json`)
5. Botão para criar as pastas no disco com `pathlib`

**Conceitos Python que Raphael vai aprender:**
- `pathlib.Path` para manipulação de caminhos
- Recursividade para renderizar árvore de pastas
- `os.makedirs` para criar estrutura no disco

---

## Notas de Tutoria

- Raphael escreve cada linha de código — sem Claude Code
- Tutor explica conceito, Raphael escreve, tutor revisa
- Correções de inglês feitas ao final de cada sessão
- Inglês praticado durante as sessões de código
- Commits feitos ao final de cada funcionalidade concluída
- Não corrija português
