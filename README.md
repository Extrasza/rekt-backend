# 🎮 REKT Game

## Descrição

Este projeto contém uma APIs RESTful que trabalham em conjunto para o gerenciamento de backlog:

- Adicionar jogos à lista;
- Listar jogos de um usuário;
- Atualizar o status de um jogo (jogado ou não);
- Remover jogos da lista.

---

## 🚀 Como Executar

### ✅ Requisitos

- Python 3.8+
- Pip
- Docker

---

## 🔧 Instalação Local

1. Clone este repositório:

```bash
git clone https://github.com/extrasza/rekt-backend.git
cd rekt-backend

2. Instale as dependencias:

```bash
pip install -r requirements.txt
```

### 3. Utilizando Containers
```bash
docker build -t rekt-backend .
docker run -p 5000:5000 rekt-backend
```
Este comando faz com que a aplicação esteja disponível no navegador, acessível pelo endereço http://localhost:5000/
