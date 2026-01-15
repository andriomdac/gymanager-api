# Conegundes – Gestão de Academias

Sistema de gestão de alunos e financeiro para academias e similares.  
Projeto completo, funcional e containerizado.

## Visão Geral
- **gymanager-api**: API com regras de negócio e dados.
- **gymanager-web**: Interface administrativa em Django.

## Execução (Docker)

**Pré-requisitos**
- Docker
- Docker Compose

```bash
git clone https://github.com/andriomdac/gym-manager-api.git
cd gym-manager-api
docker-compose up --build
```

Acesso:
```
http://localhost:8001

usuário: admin
senha: admin
```

## Tecnologias
- Python
- Django / Django REST Framework
- Docker / Docker Compose
- Banco relacional (Django ORM)
- HTML + CSS

## Funcionalidades
- Gestão de alunos
- Matrículas e status financeiro
- Pagamentos e histórico
- Controle de caixa
- Dashboard financeiro

## Demonstração
📊 Resumo Financeiro Mensal
<img width="1796" height="914" alt="ResumoMensalFinanceiro" src="https://github.com/user-attachments/assets/e1676eb9-e03c-4df9-9609-9e874211cdf7" />
💳 Novo Pagamento
<img width="1556" height="916" alt="NovoPagamento" src="https://github.com/user-attachments/assets/f4396924-4022-41f7-83cc-4eeb9fce8353" />
📝 Matrícula de Aluno
<img width="1399" height="912" alt="Matricular" src="https://github.com/user-attachments/assets/4d5d9825-afbe-4e97-929c-408ddfc6fa63" />
👥 Lista de Alunos
<img width="1493" height="917" alt="ListaAlunos" src="https://github.com/user-attachments/assets/d52c855b-b06a-4ef1-a05d-37ed1ece6120" />
📜 Histórico de Pagamentos
<img width="1513" height="911" alt="HistóricoPagamentos" src="https://github.com/user-attachments/assets/eb6e5fbb-edb4-47a5-9c0e-2a29ca70ad4c" />
💼 Histórico de Caixas
<img width="1753" height="916" alt="HistóricoCaixas" src="https://github.com/user-attachments/assets/69552aaf-49b1-4c98-8f9f-ff4a2d2710ca" />
🔍 Detalhes do Caixa
<img width="1819" height="920" alt="DetalhesCaixa" src="https://github.com/user-attachments/assets/44c2de41-d98e-43cd-9b7a-6a4088766b55" />
✅ Detalhes do Aluno (Em dia)
<img width="1556" height="913" alt="DetalhesAlunoEmDia" src="https://github.com/user-attachments/assets/5dd024ff-81a5-4c6f-ac7d-4f1e1b8c3489" />
⚠️ Detalhes do Aluno (Em atraso)
<img width="1521" height="923" alt="DetalhesAlunoAtraso" src="https://github.com/user-attachments/assets/659c2280-041f-46bc-964e-27c57d255c76" />
➕ Adicionar Valor ao Pagamento
<img width="1682" height="934" alt="AdicionarValorPagamento" src="https://github.com/user-attachments/assets/5c9dece4-c5e6-4e95-87d7-568bc8a80a23" />

## Licença
Uso livre para estudo e demonstração.  
Autor: andriomdac
# gymanager-api
