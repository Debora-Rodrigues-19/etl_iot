# 🔄 ETL de Sensores ThingsBoard para MariaDB

Este projeto realiza a extração de dados de sensores conectados à plataforma **ThingsBoard**, transforma os dados (normaliza chaves, converte timestamp) e os carrega em uma tabela `sensores` de um banco **MariaDB**.

---

## 🚀 Funcionalidades

- Autenticação na API do ThingsBoard (via REST)
- Coleta de dados de telemetria dos sensores
- Padronização dos campos (ex: `temperature` → `temperatura`)
- Conversão de timestamp UNIX para `data` e `hora`
- Inserção dos dados normalizados em um banco MariaDB
- Interface de linha de comando com `click` (parâmetros do ThingsBoard e do banco)

---

## 🧱 Requisitos

- Python 3.8+
- ThingsBoard com sensores já registrados
- Banco de dados MariaDB/MySQL com tabela `sensores` criada

---

## 📦 Instalação

1. Clone este repositório:
```bash
git clone https://github.com/Debora-Rodrigues-19/etl_iot/blob/main/etl_iot.py
cd etl-thingsboard-mariadb
````

2. Instale as dependências:

```bash
pip install requests mysql-connector-python click
```

---

## 🗃️ Estrutura da tabela `sensores`

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

Você pode executar o ETL de forma manual via CLI com os parâmetros:

```bash
python etl.py \
  --username debora9rodrigues@gmail.com \
  --password senha@123# \
  --tb-url http://home-automation.lonk-chinstrap.ts.net:8080 \
  --db-user root \
  --db-password casaos \
  --db-host 100.121.241.59 \
  --db-port 3307 \
  --db-name Iot
```

Ou de forma interativa (ele irá pedir os dados no terminal):

```bash
python etl.py
```

---

## 📁 Exemplo de saída

```bash
⏳ Iniciando coleta de dados de http://home-automation.lonk-chinstrap.ts.net:8080 com usuário 'debora9rodrigues@gmail.com'
2 linha(s) inserida(s) com sucesso.
```

---

## 🧠 Parametrização CLI

| Parâmetro       | Descrição                           |
| --------------- | ----------------------------------- |
| `--username`    | Usuário do ThingsBoard              |
| `--password`    | Senha do ThingsBoard                |
| `--tb-url`      | URL da instância do ThingsBoard     |
| `--db-user`     | Usuário do banco MariaDB            |
| `--db-password` | Senha do banco                      |
| `--db-host`     | Host do banco (padrão: `localhost`) |
| `--db-port`     | Porta do banco (padrão: `3306`)     |
| `--db-name`     | Nome do banco de dados              |

---

## ⏱️ Agendamento

Você pode usar ferramentas como:

* `cron` (Linux/macOS)
* `schedule` (Python – se ativado no script)

---

## ✨ Contribuições

Sugestões e melhorias são bem-vindas!

---

## 🛡️ Licença

MIT License

