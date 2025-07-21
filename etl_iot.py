import click
import requests
import mysql.connector
from datetime import datetime

# Dispositivos fixos (ThingsBoard device_id → nome)
dispositivos = {
    "sensor_ambiente_externo": "5b15f620-631e-11f0-a435-0721ea7777c7",
    "sensor_ambiente_interno": "aadfcc60-c23a-11ef-b046-0502d2f0cb2b"
}

# === INSERÇÃO NO BANCO ===
def inserir_dados(dados_telemetria, db_config):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    for row in dados_telemetria:
        dt = datetime.fromtimestamp(row["timestamp"] / 1000)
        data = dt.date()
        hora = dt.time()

        colunas = ["device_id", "sensor", "`timestamp`", "data", "hora"]
        valores = [row["device_id"], row["sensor"], row["timestamp"], data, hora]

        campos_sensor = ["temperatura", "umidade", "chuva_digital", "chuva_analog", "gas", "movimento"]
        for campo in campos_sensor:
            if campo in row and row[campo] is not None:
                colunas.append(campo)
                valores.append(row[campo])

        placeholders = ", ".join(["%s"] * len(valores))
        colunas_sql = ", ".join(colunas)
        query = f"INSERT INTO sensores ({colunas_sql}) VALUES ({placeholders})"
        cursor.execute(query, valores)

    conn.commit()
    cursor.close()
    conn.close()
    print(f"{len(dados_telemetria)} linha(s) inserida(s) com sucesso.")

# === CLI COM CLICK ===
@click.command()
@click.option('--username', prompt=True, help='Usuário da ThingsBoard')
@click.option('--password', prompt=True, hide_input=True, help='Senha da ThingsBoard')
@click.option('--tb-url', prompt='URL do ThingsBoard', help='URL da instância ThingsBoard')
@click.option('--db-user', prompt='Usuário do banco', help='Usuário do banco MariaDB')
@click.option('--db-password', prompt=True, hide_input=True, help='Senha do banco MariaDB')
@click.option('--db-host', default='localhost', help='Host do banco (padrão: localhost)')
@click.option('--db-port', default=3306, help='Porta do banco (padrão: 3306)')
@click.option('--db-name', prompt='Nome do banco', help='Nome do banco de dados')
def main(username, password, tb_url, db_user, db_password, db_host, db_port, db_name):
    print(f"⏳ Iniciando coleta de dados de {tb_url} com usuário '{username}'")

    # Constrói configuração do banco com os parâmetros do CLI
    db_config = {
        'user': db_user,
        'password': db_password,
        'host': db_host,
        'port': db_port,
        'database': db_name
    }

    auth_url = f"{tb_url}/api/auth/login"
    auth_payload = {"username": username, "password": password}
    auth_response = requests.post(auth_url, json=auth_payload)

    if auth_response.status_code == 200:
        token = auth_response.json()["token"]
        headers = {
            "Content-Type": "application/json",
            "X-Authorization": f"Bearer {token}"
        }

        dados_telemetria = []

        for nome_sensor, device_id in dispositivos.items():
            telemetry_url = f"{tb_url}/api/plugins/telemetry/DEVICE/{device_id}/values/timeseries"
            response = requests.get(telemetry_url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                if data:
                    sensor_row = {
                        "device_id": device_id,
                        "sensor": nome_sensor,
                        "timestamp": None
                    }

                    for valores in data.values():
                        if valores:
                            sensor_row["timestamp"] = valores[0]["ts"]
                            break

                    mapa_chaves = {
                        "temperature": "temperatura",
                        "humidity": "umidade"
                    }

                    for chave, valores in data.items():
                        if valores:
                            valor = valores[0]["value"]
                            chave_normalizada = mapa_chaves.get(chave, chave)
                            try:
                                sensor_row[chave_normalizada] = float(valor)
                            except ValueError:
                                sensor_row[chave_normalizada] = None

                    dados_telemetria.append(sensor_row)
                else:
                    print(f"⚠️ Nenhum dado de telemetria para {nome_sensor}")
            else:
                print(f"❌ Erro ao obter telemetria para {nome_sensor}: {response.text}")

        if dados_telemetria:
            inserir_dados(dados_telemetria, db_config)
        else:
            print("⚠️ Nenhum dado para inserir.")
    else:
        print("❌ Erro ao autenticar no ThingsBoard:", auth_response.text)

# === EXECUÇÃO ===
if __name__ == '__main__':
    main()
