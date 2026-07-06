<div align="center">

# ✨ Lumina

**Converse com seus PDFs. Respostas fundamentadas nos seus documentos — com fontes.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Feito%20com-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/RAG-LangChain-1C3C3C)](https://www.langchain.com/)
[![Groq](https://img.shields.io/badge/LLM-Groq-F55036)](https://groq.com/)
[![Licença](https://img.shields.io/badge/Licen%C3%A7a-MIT-blue.svg)](#licença)

[English 🇺🇸](./README.md)

</div>

---

## Visão geral

**Lumina** é um app de RAG (Retrieval-Augmented Generation) construído com Streamlit.
Você envia PDFs e o Lumina transforma tudo em uma base de conhecimento pesquisável — cada resposta volta com o arquivo e a página de onde a informação foi extraída.

Sem citações inventadas e sem vazamento entre usuários: cada sessão do navegador tem sua própria base isolada.

## Funcionalidades

- 📄 **Upload de múltiplos PDFs** — direto pela barra lateral
- 🧠 **Busca semântica** — embeddings + vector store Chroma, sem depender de palavras-chave exatas
- 💬 **Chat conversacional** — faça perguntas de acompanhamento naturalmente
- 📚 **Citações automáticas** — cada resposta mostra *nome do arquivo* + *número da página*
- 🔒 **Isolamento por sessão** — uma base por sessão de navegador; nada se mistura entre usuários
- ⚡ **Inferência rápida** — API de baixa latência do Groq

## Stack

| Camada             | Tecnologia                                                             |
| ------------------ | ---------------------------------------------------------------------- |
| Interface          | Streamlit                                                              |
| Orquestração RAG   | LangChain                                                              |
| LLM                | Groq (via `langchain-groq`)                                            |
| Embeddings         | `sentence-transformers/all-MiniLM-L6-v2` (via `langchain-huggingface`) |
| Vector store       | Chroma                                                                 |
| Extração de PDF    | pdfplumber                                                             |

## Início rápido

### Pré-requisitos

- Python **3.10+**
- Uma **chave de API do Groq** — pegue em [console.groq.com](https://console.groq.com/)

### Instalar e rodar

```bash
# 1. Clone
git clone https://github.com/seu-usuario/lumina.git
cd lumina

# 2. Crie um virtualenv
python -m venv .venv
source .venv/bin/activate           # Windows: .venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Adicione sua chave de API
echo "GROQ_API_KEY=sua_chave_aqui" > .env

# 5. Rode
streamlit run app.py
```

O app abre em **http://localhost:8501**.

> ⚠️ O `.env` já está no `.gitignore` — **nunca commite sua chave de API**.

## Como usar

1. **Envie** um ou mais PDFs pela barra lateral.
2. Clique em **"Add to library"** para indexá-los.
3. **Pergunte** no chat sobre o conteúdo.
4. Cada resposta traz chips com **arquivo** e **página** de origem.
5. Use **"Clear conversation"** para limpar o histórico e resetar a base da sessão.

## Deploy no Streamlit Community Cloud

1. Suba o repositório para o GitHub (sem `.env`, `uploads/` e `chroma_db/` — veja `.gitignore`).
2. Em [share.streamlit.io](https://share.streamlit.io), crie um novo app apontando para o repositório.
3. Em **Settings → Secrets**, adicione:

   ```toml
   GROQ_API_KEY = "sua_chave_aqui"
   ```

4. Faça o deploy. As pastas de upload e o vector store são recriadas a cada execução — o armazenamento é **efêmero** e não persiste entre reinícios.

## Estrutura do projeto

```text
lumina/
├── app.py               # Interface Streamlit e orquestração
├── utils.py             # Upload, extração e chunking de PDFs
├── embeddings.py        # Modelo de embeddings (cacheado)
├── vector_store.py      # Leitura/escrita no Chroma
├── rag.py               # Chain de RAG (retrieval + Groq)
├── config.py            # Diretórios, modelos, constantes
├── styles/
│   ├── loader.py        # Injeta o CSS customizado
│   └── style.css        # Estilos visuais do Lumina
├── requirements.txt
└── .gitignore
```

## Limitações conhecidas

- Armazenamento (PDFs + vector store) é **por sessão** e **não persistente** — reiniciar o app apaga os dados indexados.
- Sem persistência entre usuários: cada sessão começa do zero.
- Pensado para **sessões pontuais de Q&A**, não como repositório permanente de documentos.

## Roadmap

- [ ] Persistência opcional via vector store hospedado (Chroma Cloud, Pinecone)
- [ ] Suporte a outros formatos (`.docx`, `.txt`, `.md`)
- [ ] Exportar histórico de conversa
- [ ] Suporte a respostas em múltiplos idiomas
- [ ] Filtro por documento na etapa de retrieval

## Contribuindo

Issues e PRs são bem-vindos. Para mudanças maiores, abra uma issue antes para discutirmos.

## Licença

MIT — veja [LICENSE](./LICENSE).

---

<div align="center">
Feito com muito amor 💟
</div>