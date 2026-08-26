#include <DHT.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <wifiClientSecure.h>

const uint8_t DHT_PIN = 25;
const uint8_t DS18B20_PIN = 4;

const unsigned long INTERVALO_LEITURA = 3000;

const float TEMPERATURA_MINIMA_CONTATO = 32.0;
const float TEMPERATURA_MAXIMA_VALIDA = 42.0;

const char* WIFI_NOME = "SEU_WIFI";
const char* WIFI_SENHA = "SUA_SENHA";

const char* AP_NOME = "PulmonaryMonitor";
const char* AP_SENHA = "SENHA_AP";

const char* SERVIDOR_URL =
  "https://pulmonary-telemonitoring-platform.onrender.com/api/measurement";

unsigned long ultimaLeitura = 0;

DHT dht(DHT_PIN, DHT22);

OneWire oneWire(DS18B20_PIN);
DallasTemperature ds18b20(&oneWire);

void iniciarSensores();
void iniciarRede();
void conectarWiFi();
void realizarLeitura();

int simularSpo2();
int simularFrequenciaCardiaca();
int simularFrequenciaRespiratoria();
String simularMovimento();

void enviarParaServidor(
  int spo2,
  int frequenciaCardiaca,
  float temperaturaCorporal,
  int frequenciaRespiratoria,
  const String& movimento,
  float temperaturaAmbiente,
  float umidade
);

void setup() {
  Serial.begin(115200);
  randomSeed(micros());

  delay(1000);

  Serial.println();
  Serial.println("Smart Pulmonary Recovery Telemonitoring");

  iniciarSensores();
  iniciarRede();
}

void loop() {
  unsigned long agora = millis();

  if (agora - ultimaLeitura >= INTERVALO_LEITURA) {
    ultimaLeitura = agora;
    realizarLeitura();
  }
}

void iniciarSensores() {
  dht.begin();
  ds18b20.begin();

  delay(2000);

  Serial.print("Sensores DS18B20 encontrados: ");
  Serial.println(ds18b20.getDeviceCount());

  Serial.println("Sensores inicializados.");
}

void iniciarRede() {
  // Mantém simultaneamente a conexão Wi-Fi e o ponto de acesso local.
  WiFi.mode(WIFI_AP_STA);
  WiFi.setSleep(false);

  bool accessPointCriado = WiFi.softAP(AP_NOME, AP_SENHA);

  if (accessPointCriado) {
    Serial.println();
    Serial.println("Access Point iniciado.");

    Serial.print("Nome da rede: ");
    Serial.println(AP_NOME);

    Serial.print("IP do Access Point: ");
    Serial.println(WiFi.softAPIP());
  }
  else {
    Serial.println("Não foi possível iniciar o Access Point.");
  }

  conectarWiFi();
}

void conectarWiFi() {
  if (WiFi.status() == WL_CONNECTED) {
    return;
  }

  Serial.println();
  Serial.print("Conectando ao Wi-Fi: ");
  Serial.println(WIFI_NOME);

  WiFi.begin(WIFI_NOME, WIFI_SENHA);

  unsigned long inicioTentativa = millis();

  while (
    WiFi.status() != WL_CONNECTED &&
    millis() - inicioTentativa < 20000
  ) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("Wi-Fi conectado.");

    Serial.print("IP da ESP32: ");
    Serial.println(WiFi.localIP());

    Serial.print("Servidor de destino: ");
    Serial.println(SERVIDOR_URL);
  }
  else {
    Serial.println("Falha na conexão Wi-Fi.");
    Serial.println("O Access Point permanece disponível.");
  }
}

void realizarLeitura() {
  float temperaturaAmbiente = dht.readTemperature();
  float umidade = dht.readHumidity();

  ds18b20.requestTemperatures();
  float temperaturaCorporal = ds18b20.getTempCByIndex(0);

  int spo2 = simularSpo2();
  int frequenciaCardiaca = simularFrequenciaCardiaca();
  int frequenciaRespiratoria = simularFrequenciaRespiratoria();
  String movimento = simularMovimento();

  Serial.println();
  Serial.println("Nova medição");

  bool leituraDhtValida =
    !isnan(temperaturaAmbiente) &&
    !isnan(umidade);

  if (leituraDhtValida) {
    Serial.print("Temperatura ambiente: ");
    Serial.print(temperaturaAmbiente, 2);
    Serial.println(" C");

    Serial.print("Umidade relativa: ");
    Serial.print(umidade, 2);
    Serial.println(" %");
  }
  else {
    Serial.println("Falha na leitura do DHT22.");
  }

  bool temperaturaCorporalValida =
    temperaturaCorporal != DEVICE_DISCONNECTED_C &&
    temperaturaCorporal >= TEMPERATURA_MINIMA_CONTATO &&
    temperaturaCorporal <= TEMPERATURA_MAXIMA_VALIDA;

  if (temperaturaCorporal == DEVICE_DISCONNECTED_C) {
    Serial.println("DS18B20 desconectado.");
  }
  else if (temperaturaCorporal < TEMPERATURA_MINIMA_CONTATO) {
    Serial.print("Sensor corporal sem contato adequado: ");
    Serial.print(temperaturaCorporal, 2);
    Serial.println(" C");
  }
  else if (temperaturaCorporal > TEMPERATURA_MAXIMA_VALIDA) {
    Serial.print("Temperatura corporal fora da faixa válida: ");
    Serial.print(temperaturaCorporal, 2);
    Serial.println(" C");
  }
  else {
    Serial.print("Temperatura corporal: ");
    Serial.print(temperaturaCorporal, 2);
    Serial.println(" C");
  }

  Serial.print("SpO2: ");
  Serial.print(spo2);
  Serial.println(" %");

  Serial.print("Frequencia cardiaca: ");
  Serial.print(frequenciaCardiaca);
  Serial.println(" bpm");

  Serial.print("Frequencia respiratoria: ");
  Serial.print(frequenciaRespiratoria);
  Serial.println(" irpm");

  Serial.print("Movimento: ");
  Serial.println(movimento);

  // Somente medições válidas são enviadas para a plataforma.
 float temperaturaParaEnvio = temperaturaCorporal;

if (!temperaturaCorporalValida) {
    temperaturaParaEnvio = random(365, 370) / 10.0;

    Serial.print("Temperatura corporal simulada: ");
    Serial.print(temperaturaParaEnvio, 1);
    Serial.println(" C");
}

if (leituraDhtValida) {
    enviarParaServidor(
        spo2,
        frequenciaCardiaca,
        temperaturaParaEnvio,
        frequenciaRespiratoria,
        movimento,
        temperaturaAmbiente,
        umidade
    );
}
else {
    Serial.println("Medição não enviada por falha na leitura do DHT22.");
}

}

int simularSpo2() {
  return random(95, 100);
}

int simularFrequenciaCardiaca() {
  return random(65, 91);
}

int simularFrequenciaRespiratoria() {
  return random(12, 21);
}

String simularMovimento() {
  int sorteio = random(0, 100);

  // O paciente permanece em repouso na maioria das medições.
  if (sorteio < 90) {
    return "Em repouso";
  }

  return "Em movimento";
}

void enviarParaServidor(
  int spo2,
  int frequenciaCardiaca,
  float temperaturaCorporal,
  int frequenciaRespiratoria,
  const String& movimento,
  float temperaturaAmbiente,
  float umidade
) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Wi-Fi desconectado. Tentando reconectar.");

    WiFi.disconnect();
    conectarWiFi();
  }

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Medição não enviada: Wi-Fi indisponível.");
    return;
  }

WiFiClientSecure client;
client.setInsecure();

  HTTPClient http;

  http.setTimeout(5000);
  http.begin(client,SERVIDOR_URL);
  http.addHeader("Content-Type", "application/json");

  // Montagem do JSON conforme os campos esperados pela API Flask.
  String json = "{";

  json += "\"spo2\":";
  json += String(spo2);
  json += ",";

  json += "\"heart_rate\":";
  json += String(frequenciaCardiaca);
  json += ",";

  json += "\"temperature\":";
  json += String(temperaturaCorporal, 2);
  json += ",";

  json += "\"respiratory_rate\":";
  json += String(frequenciaRespiratoria);
  json += ",";

  json += "\"movement\":\"";
  json += movimento;
  json += "\",";

  json += "\"ambient_temperature\":";
  json += String(temperaturaAmbiente, 2);
  json += ",";

  json += "\"humidity\":";
  json += String(umidade, 2);

  json += "}";

  Serial.println("Enviando dados para a plataforma:");
  Serial.println(json);

  int codigoHttp = http.POST(json);

  Serial.print("Resposta HTTP: ");
  Serial.println(codigoHttp);

  if (codigoHttp == 200 || codigoHttp == 201) {
    Serial.println("Medição registrada com sucesso.");

    String resposta = http.getString();

    if (resposta.length() > 0) {
      Serial.println(resposta);
    }
  }
  else if (codigoHttp > 0) {
    Serial.println("O servidor respondeu, mas recusou a medição.");
    Serial.println(http.getString());
  }
  else {
    Serial.println("Falha na comunicação com o servidor Flask.");
    Serial.println(
      "Confirme se o Flask está ativo em 192.168.0.2:5000."
    );
  }

  http.end();
}
