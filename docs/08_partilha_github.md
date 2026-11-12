# Primeira submissão da Fase 2 ao GitHub (Windows / PowerShell)

**Objetivo:** publicar a **versão organizada da Fase 2** na branch de trabalho e integrá-la em `develop` por Pull Request, **não diretamente em `main`**. O ZIP `si-energia-fase2-github.zip` é o que deve ser copiado para o repositório. Não utilizar o ZIP local completo para a primeira submissão.

## 1. Pré-requisitos

- Ter Git instalado: `git --version`.
- Ter acesso ao repositório do grupo no GitHub (com permissões para criar branches e abrir PRs).
- Copiar o **URL HTTPS do repositório** (botão **Code** no GitHub); exemplo de formato: `https://github.com/UTILIZADOR/si-energia-bi-2026-2027.git`.
- Os exemplos assumem que o repositório já existe no GitHub e tem uma branch `main`, como acontece quando é criado com `README.md`.

## 2. Clonar o repositório (se ainda não está no PC)

Abrir PowerShell na pasta onde desejas guardá-lo:

```powershell
cd "$HOME\Documents"
git clone https://github.com/UTILIZADOR/si-energia-bi-2026-2027.git
cd si-energia-bi-2026-2027
git status
git remote -v
```

**Substituir `UTILIZADOR` pelo proprietário verdadeiro**. Se já tens o repositório clonado, abre o terminal na pasta existente e não o clones uma segunda vez.
