# 🔄 ETL de Sensores ThingsBoard para MariaDB

Este projeto realiza a extração de dados de sensores conectados à plataforma **ThingsBoard**, transforma os dados (normaliza chaves, converte timestamp) e os carrega em uma tabela `sensores` de um banco **MariaDB**.

---

## 🚀 Funcionalidades

- Autenticação na API do ThingsBoard (via REST)
- Coleta de dados de telemetria dos sensores
- Padronização dos campos (ex: `temperature` → `temperatura`)
- Conversão de timestamp UNIX para `data` e `hora`
- Inserção dos dados normalizados em um banco MariaDB
- Interface de linha de comando com `click` (parâmetros dinâmicos)

---

## 🧱 Requisitos

- Python 3.8+
- ThingsBoard com sensores já registrados
- Banco de dados MariaDB/MySQL com tabela `sensores` criada

---

## 📦 Instalação

1. Clone este repositório:
```bash
git clone https://github.com/Debora-Rodrigues-19/etl_iot
cd etl-thingsboard-mariadb
````

2. Instale as dependências:

```bash
pip install requests mysql-connector-python click
```

---

## 🗃️ Estrutura esperada da tabela `sensores`

```sql
CREATE TABLE sensores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_id CHAR(36),
    sensor VARCHAR(255),
    `timestamp` BIGINT,
    data DATE,
    hora TIME,
    temperatura REAL,
    umidade REAL,
    chuva_digital INT,
    chuva_analog INT,
    gas REAL,
    movimento REAL
);
```

---

## ⚙️ Como usar

### 📌 Executar manualmente

```bash
python etl.py --username seu_email@dominio.com --password sua_senha --tb-url http://seu-servidor-thingsboard:porta
```

Ou de forma interativa:

```bash
python etl.py
# será solicitado:
# - usuário
# - senha
# - URL da instância ThingsBoard
```

---

## ⏱️ Agendamento (opcional)

Para agendar a execução automática a cada 10 minutos, use:

* `cron` (Linux/macOS)
* `schedule` (Python) → versão com agendamento pode ser implementada separadamente.

---

## 📁 Exemplo de saída

```bash
⏳ Iniciando coleta de dados de http://localhost:8080 com usuário 'juanengml@gmail.com'
2 linha(s) inserida(s) com sucesso.
```

---

## ✨ Contribuições

Sugestões e melhorias são bem-vindas!!1

---

## 🛡️ Licença

MIT License.

