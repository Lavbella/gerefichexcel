# Advanced Data Engineering & Analytics
### Multi-Criteria Filtering & Transformation Pipelines

[Português](#português) | [English](#english)

---

## Licença / License
This project is licensed under the **GNU GPLv3**. See the [LICENSE](LICENSE) file for details.

---

## Português

Esta é uma aplicação desktop nativa desenvolvida em Python utilizando **Tkinter / CustomTkinter**, concebida como uma plataforma avançada de engenharia e análise de dados. A ferramenta disponibiliza pipelines robustos para filtragem e transformação multicritério de dados estruturados utilizando o poder do **pandas**, além de contar com um motor de persistência nativo para guardar e reutilizar moldes de filtragem complexos através de uma interface gráfica moderna e responsiva.

### Funcionalidades e Engenharia Central

#### UI/UX & Layout de Estado Inicial
Para proporcionar uma experiência profissional e limpa, a interface gráfica evita iniciar com um ecrã vazio. Inclui um **Modo de Estado Inicial** estruturado com 3 painéis simétricos (Volume de Dados, Filtros Ativos e Estado do Pipeline) juntamente com uma mensagem informativa que indica "Awaiting Execution...". A interface faz a transição automática para a visualização das tabelas de dados assim que a execução do pipeline é concluído.

#### Arquitetura & Engenharia do Sistema
A aplicação foi desenhada com foco em modularidade e alta performance para manipulação de dados:
*   **Pipeline de Engenharia com Pandas:** Motores de transformação que executam operações complexas de limpeza, conversão de tipos, agregações e filtragem multicritério avançada em tempo real.
*   **Persistência Nativa (Templates JSON):** Motores integrados que permitem ao utilizador guardar toda a configuração e critérios de um filtro complexo num ficheiro JSON local. Isto possibilita carregar e reexecutar o mesmo pipeline instantaneamente em novos conjuntos de dados.
*   **Módulos de Visualização e Exportação:** Exibição eficiente dos dados transformados na interface gráfica com capacidade de exportar os resultados em múltiplos formatos estruturados.

### Pré-requisitos (Ubuntu)
Antes de começar, certifique-se de que tem as dependências essenciais do sistema instaladas (especialmente o suporte para Tkinter):
```bash
sudo apt update
sudo apt install python3-pip python3-venv python3-tk git -y
```

### 1. Configurar o Ambiente Virtual (venv)
Execute estes comandos no terminal para clonar o repositório e preparar o ambiente:

```bash
# Criar o ambiente virtual
python3 -m venv venv

# Ativar o ambiente virtual
source venv/bin/activate

# Atualizar o gerenciador de pacotes e instalar os requisitos
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Executar a Aplicação em Desenvolvimento
Com o ambiente virtual (`venv`) ativo, inicie a aplicação de forma direta:
```bash
python app_dynamic.py
```

### 3. Como Gerar o Executável (Ubuntu)
Para compilar esta aplicação num único executável nativo do Linux, utilizando o ícone do projeto e ocultando a consola do terminal em segundo plano, execute o seguinte comando do PyInstaller:

```bash
# Limpar caches de compilações anteriores
rm -rf build dist

# Gerar o executável completo
pyinstaller --noconsole --onefile --icon=icons8-eid-mubarak-96.ico app_dynamic.py
```
O binário final será gerado dentro da pasta **`dist/`** com o nome `app_dynamic`. Para o iniciar diretamente pelo terminal, utilize:
```bash
./dist/app_dynamic
```

---

## English

This is a native desktop application built with Python using **Tkinter / CustomTkinter**, engineered as an advanced data engineering and analytics platform. The tool delivers robust multi-criteria data filtering and transformation pipelines powered by **pandas**, backed by native persistence engines to save and rerun complex filter templates instantly via a modern and responsive graphical user interface.

### Features & Core Components

#### UI/UX & Initial State Layout
To deliver a clean and professional user experience, the graphical dashboard avoids starting as a blank screen. It features an **Initial State Mode** structured with 3 symmetrical panels (Data Volume, Active Filters, and Pipeline Status) alongside an info status stating "Awaiting Execution...". It transitions seamlessly into data grids the moment the dataset pipeline processing completes.

#### Architecture & Core Engineering
The application focuses on architectural modularity and high performance for data manipulation:
*   **Pandas-Powered Transformation Pipelines:** Advanced data processing cores that perform complex cleanups, type conversions, aggregations, and multi-layered logical filtering on the fly.
*   **Native Persistence (JSON Templates):** Built-in configuration engines that allow users to serialize complex query parameters into local JSON-based configuration files, enabling automated instant re-runs on fresh datasets.
*   **Data Grid & Export Infrastructure:** Efficient native rendering of transformed outputs inside the Tkinter view, with options to export the final analytical datasets into multiple structured file formats.

### Prerequisites (Ubuntu)
Before starting, ensure you have the essential system dependencies installed (especially Tkinter development support):
```bash
sudo apt update
sudo apt install python3-pip python3-venv python3-tk git -y
```

### 1. Setting Up the Virtual Environment (venv)
Run these commands in your terminal to set up the isolated project environment:

```bash
# Create the virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip and install requirements
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Running the Application in Development
With the virtual environment (`venv`) active, launch the application directly:
```bash
python app_dynamic.py
```

### 3. How to Generate the Executable (Ubuntu)
To compile the Tkinter application into a single standalone Linux binary using PyInstaller, setting the project icon and hiding the background terminal console window, run:

```bash
# Clear previous build caches
rm -rf build dist

# Generate the standalone executable
pyinstaller --noconsole --onefile --icon=icons8-eid-mubarak-96.ico app_dynamic.py
```
The final standalone binary will be generated inside the **`dist/`** folder under the name `app_dynamic`. To run it, use:
```bash
./dist/app_dynamic
