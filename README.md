# 🔄 ETL de Sensores ThingsBoard para MariaDB

Este projeto realiza a extração de dados de sensores conectados à plataforma **ThingsBoard**, transforma os dados (normaliza chaves, converte timestamp) e os carrega em uma tabela `sensores` de um banco **MariaDB**.

---

## 🚀 Funcionalidades

- Autenticação na API do ThingsBoard (via REST)
- Coleta de dados de telemetria dos sensores
- Padronização dos campos (ex: `temperature` → `temperatura`)
- Conversão de timestamp UNIX para `data` e `hora`
- Inserção dos dados normalizados em um banco MariaDB
- Interface de linha de comando com `click`
- Totalmente containerizado via Docker

---

## 🧱 Requisitos

- Python 3.8+
- ThingsBoard com sensores já registrados
- Banco de dados MariaDB/MySQL acessível
- Docker instalado

---

## 📦 Instalação e Build

1. Clone o repositório:
```bash
git clone https://github.com/Debora-Rodrigues-19/etl_iot/blob/main/etl_iot.py
cd etl-thingsboard-mariadb
````

2. Build da imagem Docker:

```bash
docker build -t etl-iot-job .
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

## ⚙️ Como executar o ETL

### ✅ Execução direta com parâmetros via linha de comando

```bash
docker run --rm etl-iot-job \
  --username debora9rodrigues@gmail.com \
  --password Iot@25 \
  --tb-url http://192.168.0.48:8080 \
  --db-user root \
  --db-password casaos \
  --db-host 192.168.0.48 \
  --db-port 3307 \
  --db-name Iot
```

### 💬 Ou modo interativo:

```bash
docker run -it --rm etl-iot-job
```

---

## 🧠 Parâmetros CLI

| Parâmetro       | Descrição                          |
| --------------- | ---------------------------------- |
| `--username`    | Usuário do ThingsBoard             |
| `--password`    | Senha do ThingsBoard               |
| `--tb-url`      | URL da instância ThingsBoard       |
| `--db-user`     | Usuário do banco MariaDB           |
| `--db-password` | Senha do banco                     |
| `--db-host`     | Host do banco (ex: `192.168.0.48`) |
| `--db-port`     | Porta do banco (ex: `3307`)        |
| `--db-name`     | Nome do banco de dados             |

---

## 📁 Exemplo de saída

```bash
⏳ Iniciando coleta de dados de http://192.168.0.48:8080 com usuário 'debora9rodrigues@gmail.com'
2 linha(s) inserida(s) com sucesso.
```

---

## 🔄 Agendamento

Você pode agendar a execução deste container com:

* `cron` no host
* `watch` para testes
* `kubernetes cronjob` ou orquestradores como `Airflow`, `Dagster`, etc.

---

## 🛠️ Futuras melhorias

* Suporte a `.env` e `docker-compose`
* Agendamento interno com `schedule`
* Exportação para formatos CSV/Parquet

---

## 🛡️ Licença

MIT License

```
