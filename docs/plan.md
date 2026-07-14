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

### Ambiente de Desenvolvimento
Migrado do WSL2 (Linux) para Windows nativo após problema de virtualização. Diferenças tratadas via `pathlib` para caminhos. Comando de execução: `python -m streamlit run app.py`.

---

## Fluxo do Produto — REVISADO

> **Mudança importante de fluxo:** a criação de estrutura de pastas passou a depender do scan. O usuário informa o projeto, scanneia os arquivos, e a estrutura de pastas é criada com base nas disciplinas encontradas — não antes.

### FASE 1 — Configuração (feita uma vez)

**Etapa 1 — Padrão de nomenclatura**
Usuário cola trecho do procedimento da empresa. Haiku 4.5 interpreta e extrai o padrão. Suporta múltiplos padrões. Usuário confirma antes de salvar.

### FASE 2 — Por projeto

**Etapa 2 — Cadastro do projeto**
Usuário informa nome, ano e caminho da pasta do projeto. App valida se o caminho existe no disco. Salva em `config/projects/{name}.json`.

**Etapa 3 — Scan e classificação**
Scanner percorre a pasta do projeto. Classifier identifica disciplina, tipo, área, revisão pelo nome do arquivo. Stamp reader (Tesseract local) lê carimbo dos arquivos sem revisão no nome.

**Etapa 4 — Criação da estrutura de pastas**
Com base nas disciplinas encontradas no scan, app sugere a estrutura:
```
Documentação Técnica/
├── Lista Mestra
├── {year} - {project name}/
│   ├── Lista do Projeto
│   ├── CIV/
│   │   ├── OLD/
│   │   └── arquivos...
│   ├── ELE/
│   │   ├── OLD/
│   │   └── arquivos...
│   └── (outras disciplinas encontradas)/
│       ├── OLD/
│       └── arquivos...
```
Usuário confirma ou ajusta. App cria as pastas no disco com `pathlib`.

**Etapa 5 — Destino e origem**
Usuário escolhe pasta de destino e define escopo da operação.

**Etapa 6 — Gestão de revisões**
App compara arquivos novos com existentes no destino pelo código base. Se detectar revisão: pergunta onde mover o arquivo antigo (OLD/). Pergunta se quer fixar esse diretório como padrão.

**Etapa 7 — Revisão e aprovação**
Tabela editável: arquivo → nome sugerido → pasta de destino → ação. Usuário aprova antes de qualquer movimentação.

**Etapa 8 — Execução segura**
Default: cria cópia do projeto antes de executar. Exibe alerta de risco para edição direta. Gera log completo da operação.

**Etapa 9 — Lista de documentos versionada**
Gerada automaticamente após cada operação. Salva como `Lista_Docs_v01.xlsx`, `v02`... Lista Mestra gerada na raiz de Documentação Técnica.

### Disciplinas suportadas (OTTS-016)
CIV, CON, COM, ELE, GEO, HSE, INC, MEC, PIP, TEL, PCS, MAR, QAC, OPM, PMT, PRM, BAS, CAL, CEC, CER, DIA, DST, DWG, GTC, HMB, ISO, IRV, LIS, MNL, PID, PFD, PHY, PRC, PLD, PRO, REP, RFQ, SPE, SOC, TRA, TOR, TQR, VAR

---

## Arquitetura de Módulos

```
engineering-doc-organizer/
├── app.py                          # Entry point Streamlit
├── config/
│   ├── settings.py                 # Constantes globais
│   ├── projects/                   # JSONs dos projetos salvos
│   └── standards/                  # JSONs dos padrões salvos
├── core/
│   ├── models.py                   # EngineeringFile, Project
│   ├── scanner.py                  # Scan recursivo de pastas
│   ├── classifier.py               # Classificação por regex
│   ├── standard_extractor.py       # Extração de padrão de nomenclatura
│   ├── project_manager.py          # CRUD de projetos
│   ├── suggestion_engine.py        # (pendente)
│   ├── renamer.py                  # (pendente)
│   └── stamp_reader.py             # (pendente)
├── ui/
│   └── pages/
│       ├── config_page.py          # Padrão de nomenclatura ✓
│       ├── project_page.py         # Cadastro de projeto ✓ (Sprint 5)
│       ├── folder_page.py          # Estrutura de diretórios (pendente)
│       ├── scan_page.py            # Scan + classificação (pendente)
│       ├── review_page.py          # Revisão e aprovação (pendente)
│       └── apply_page.py           # Execução e log (pendente)
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
| Sprint 5 | 🔨 Em andamento | project_page + project_manager — cadastro de projeto com validação de path |
| Sprint 6 | ⏳ Pendente | scan_page — integração Scanner + Classifier + Tesseract |
| Sprint 7 | ⏳ Pendente | folder_page — criação de estrutura baseada nas disciplinas do scan |
| Sprint 8 | ⏳ Pendente | Stamp reader — Tesseract local, leitura de carimbo PDF/DWG |
| Sprint 9 | ⏳ Pendente | Gestão de revisões — detecção, mover obsoletos, padrão OLD/ |
| Sprint 10 | ⏳ Pendente | Review page + execução segura — tabela editável, log, cópia |
| Sprint 11 | ⏳ Pendente | Lista de documentos versionada — openpyxl, Lista Mestra |
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
  - Gestão de session_state com dynamic keys (text_key, upload_key)
  - Validações: nome obrigatório, nome único antes de salvar
  - Auto-seleção do padrão recém-salvo no dropdown

### Sprint 5 (em andamento)
- **Decisão de fluxo:** criação de pastas passa a depender do scan — app cria estrutura com base nas disciplinas encontradas, não antes
- **Estrutura de pastas definida:** `Documentação Técnica / {year} - {project} / {DISCIPLINA} / OLD /`
- `core/project_manager.py`:
  - `save_project(name, year, path)` — salva JSON em `config/projects/{name}.json`
  - `list_projects()` — lista projetos salvos
  - `load_project(name)` — carrega JSON de um projeto
  - `delete_project(name)` — remove JSON de um projeto
- `ui/pages/project_page.py`:
  - Seção "Saved Projects" com dropdown e botão Delete
  - Seção "New Project" com campos name, year, path
  - Validações: campos obrigatórios, nome único, path existente no disco
  - Dynamic keys para limpeza de inputs
- `app.py`: adicionada rota para `project_page` no sidebar

---

## Próximos Passos — Sprint 5 (continuação)

1. Testar `project_page.py` — salvar projeto, validar path, auto-selecionar no dropdown
2. Adicionar visualização do projeto selecionado (nome, ano, path) ao selecionar no dropdown
3. Commitar Sprint 5 completo
4. Iniciar Sprint 6 — `scan_page.py`

---

## Notas de Tutoria

- Raphael escreve cada linha de código — sem Claude Code
- Tutor explica conceito, Raphael escreve, tutor revisa
- Correções de inglês feitas ao final de cada sessão
- Inglês praticado durante as sessões de código
- Commits feitos ao final de cada funcionalidade concluída
- Não corrija português
- Ambiente: Windows nativo, VS Code, terminal PowerShell integrado
- Comando de execução: `python -m streamlit run app.py`
