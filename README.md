# Enterprise Computer Vision & Speech Architecture with Streamlit

Aplicação robusta e modular de Visão Computacional e Processamento de Áudio (Speech to Text) integrada ao banco de dados relacional Serverless Neon.tech, pronta para execução em ambiente local e produção via Render.

## 🚀 Tecnologias Empregadas

- **Python 3.12+**
- **Streamlit**: Criação de interfaces reativas em tempo real.
- **OpenCV & Pillow**: Processamento digital de imagens, matrizes matemáticas e filtros de nitidez/luminosidade.
- **Faster-Whisper**: Transcrição local otimizada baseada na arquitetura Whisper da OpenAI.
- **SQLAlchemy**: Camada ORM estável com suporte ao driver assíncrono/síncrono `psycopg`.
- **Neon.tech (PostgreSQL)**: Banco de dados relacional escalável com conexão SSL.

---

## 🏢 Arquitetura do Sistema

O projeto segue as diretrizes de **Arquitetura Limpa** e **SOLID**, dividindo responsabilidades claras em camadas distintas:

1. **Camada de Apresentação (`components/`, `app.py`)**: Responsável exclusiva pela renderização visual de entradas e saídas de dados.
2. **Camada de Orquestração (`controllers/`)**: Atua como intermediária de fluxo, delegando tarefas complexas aos serviços e chamadas de persistência ao repositório.
3. **Camada de Regras de Negócio e Serviços (`services/`)**: Centraliza os pipelines pesados de inteligência artificial e matemática de imagem (OpenCV, Whisper).
4. **Camada de Acesso a Dados (`repositories/`, `models/`, `database/`)**: Isola transações SQL do restante da aplicação, assegurando baixo acoplamento.

---

## 🔧 Configuração e Execução Local

Como premissa de desenvolvimento ágil, este projeto **dispensa o isolamento de ambientes virtuais (venv)**, instalando os pacotes necessários diretamente no escopo global ou de contêineres do sistema operacional.

### 1. Clonar o repositório e acessar a pasta
```bash
git clone <url-do-seu-repositorio>
cd computer-vision-streamlit