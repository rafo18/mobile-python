# 📱 Mobile Automation Framework - Python

Framework de automatización de pruebas desarrollado en **Python**, utilizando **Behave, Appium, Requests, Oracle Database, LambdaTest, BrowserStack y Allure Reports**.

El framework permite automatizar y validar diferentes capas de una aplicación:

- 📱 Automatización Mobile
- 🌐 Automatización de APIs REST
- 🗄️ Automatización de Base de Datos Oracle
- 🔗 Pruebas de integración Mobile + API + Database
- ☁️ Ejecución en dispositivos reales mediante LambdaTest
- ☁️ Ejecución en dispositivos reales mediante BrowserStack
- 🔐 BrowserStack Local para aplicaciones/servicios accesibles únicamente desde una red privada
- 📱 Ejecución multi-device
- 🥒 BDD utilizando Gherkin
- 📊 Reportes con Allure
- 📸 Evidencia automática mediante screenshots
- ⚙️ Configuración mediante variables de entorno

---

# 🚀 Características

## 📱 Mobile Automation

Automatización de aplicaciones móviles utilizando Appium.

Soporta:

- Android
- iOS
- Ejecución local
- LambdaTest
- BrowserStack
- BrowserStack Local
- Emuladores
- Dispositivos reales
- Ejecución en múltiples dispositivos
- Captura automática de screenshots
- Page Object Model

---

## ☁️ Proveedores de ejecución Mobile

El framework utiliza un único `driver_factory.py` para seleccionar el proveedor mediante `EXECUTION_PLATFORM`.

```text
                    Driver Factory
                          │
          ┌───────────────┼───────────────┐
          │               │               │
        LOCAL         LAMBDATEST       BROWSERSTACK
          │               │               │
       Appium         Real Device      Real Device
                                          │
                                          ▼
                                  BrowserStack Local
                                          │
                                          ▼
                                   Red corporativa
```

### Local

```env
EXECUTION_PLATFORM=local
PLATFORM_NAME=Android
```

### LambdaTest

```env
EXECUTION_PLATFORM=lambdatest
PLATFORM_NAME=Android
```

### BrowserStack

```env
EXECUTION_PLATFORM=browserstack
PLATFORM_NAME=Android
```

---

# 🌐 BrowserStack

El framework permite ejecutar aplicaciones nativas mediante Appium en BrowserStack.

Configuración básica:

```env
EXECUTION_PLATFORM=browserstack
PLATFORM_NAME=Android

BS_USERNAME=
BS_ACCESS_KEY=
BS_APP=bs://YOUR_APP_ID
BS_DEVICE_INDEX=0
```

La aplicación debe estar subida a BrowserStack App Automate y utilizar el identificador `bs://...` proporcionado por BrowserStack.

Las credenciales deben mantenerse únicamente en `.env`.

---

# 🔐 BrowserStack Local

BrowserStack Local permite que los dispositivos remotos de BrowserStack accedan a aplicaciones, APIs y servicios disponibles únicamente desde una red privada, VPN o red corporativa.

Configuración:

```env
BS_LOCAL=true
BS_LOCAL_IDENTIFIER=mobile-automation-local
```

El framework utiliza el paquete `browserstack-local` para iniciar y detener el túnel automáticamente durante la ejecución.

Flujo:

```text
Behave
   ↓
before_all()
   ↓
BrowserStack Local START
   ↓
BrowserStack Device
   ↓
VPN / Red corporativa
   ↓
API / Backend interno
   ↓
after_all()
   ↓
BrowserStack Local STOP
```

### Instalación

```bash
pip install browserstack-local
```

Actualizar dependencias después de instalar una nueva librería:

```bash
pip freeze > requirements.txt
```

---

# 📱 Configuración de dispositivos

Los dispositivos de cada proveedor se mantienen separados en:

```text
config/devices.py
```

Ejemplo:

```python
LAMBDATEST_ANDROID_DEVICES = [
    {
        "name": "Galaxy S26",
        "platform_version": "16"
    },
    {
        "name": "Galaxy S24",
        "platform_version": "14"
    }
]

BROWSERSTACK_ANDROID_DEVICES = [
    {
        "name": "Samsung Galaxy S23 Ultra",
        "platform_version": "13.0"
    }
]
```

BrowserStack debe utilizar únicamente nombres/versiones disponibles para la cuenta.

LambdaTest utiliza:

```env
LT_DEVICE_INDEX=0
```

BrowserStack utiliza:

```env
BS_DEVICE_INDEX=0
```

---

# 📱 Multi-device

El proyecto incluye:

```text
run_devices.py
```

El runner detecta automáticamente el proveedor mediante:

```env
EXECUTION_PLATFORM=browserstack
```

o:

```env
EXECUTION_PLATFORM=lambdatest
```

También permite recibir el tag desde la terminal.

### Smoke

```bash
python run_devices.py @smoke
```

### Login

```bash
python run_devices.py @login
```

### API

```bash
python run_devices.py @api
```

### Database

```bash
python run_devices.py @database
```

### Integration

```bash
python run_devices.py @integration
```

Si no se especifica un tag:

```bash
python run_devices.py
```

se ejecuta `@smoke` por defecto.

El runner:

1. Limpia `allure-results`.
2. Selecciona la lista de dispositivos del proveedor.
3. Define automáticamente `LT_DEVICE_INDEX` o `BS_DEVICE_INDEX`.
4. Ejecuta Behave para cada dispositivo.
5. Separa los resultados temporales.
6. Agrega Device, Platform, Version, Execution y Tag a Allure.
7. Genera un `historyId` independiente por proveedor y dispositivo.
8. Consolida los resultados en un único `allure-results`.

---

# 🌐 API Automation

Automatización de APIs REST utilizando `Requests`.

Actualmente el framework soporta:

- GET
- POST
- PUT
- DELETE

La arquitectura permite agregar posteriormente:

- PATCH
- Bearer Token
- API Key
- Basic Authentication
- Headers comunes
- Manejo de tokens

Las llamadas API pueden generar evidencia para Allure:

```text
API Method
API Endpoint
API Parameters
API Headers
API Body
API Status Code
API Response
```

---

# 🌍 Múltiples APIs / Dominios

El framework permite trabajar con diferentes dominios y reutilizar el mismo `ApiClient`.

Ejemplo:

```env
POKEMON_API_URL=https://pokeapi.co/api/v2
TEST_API_URL=https://jsonplaceholder.typicode.com
```

Para nuevos dominios se pueden agregar variables en `.env` y configurarlas desde:

```text
config/api_config.py
```

Las operaciones específicas de negocio se implementan en clases dentro de:

```text
api/
```

Ejemplo:

```text
api/
├── auth_api.py
├── transfer_api.py
├── qr_api.py
└── pokemon_api.py
```

Cada clase reutiliza el mismo cliente HTTP.

---

# 📡 Ejemplo GET

```python
response = context.pokemon_api.get_pokemon(
    "pikachu"
)
```

# 📡 Ejemplo POST

```python
body = {
    "title": "Mobile Automation",
    "body": "Prueba automatizada con Python",
    "userId": 1
}

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

response = context.test_api.create_post(
    body=body,
    headers=headers
)
```

# 📡 Ejemplo PUT

```python
body = {
    "name": "Updated User",
    "email": "user@test.com"
}

response = context.test_api.update_user(
    user_id=1,
    body=body
)
```

# 📡 Ejemplo DELETE

```python
response = context.test_api.delete_user(
    user_id=1
)
```

---

# 🗄️ Database Automation

Integración con Oracle Database utilizando `oracledb`.

Permite ejecutar:

- SELECT
- INSERT
- UPDATE
- DELETE

La arquitectura utiliza Repository Pattern:

```text
Test Step
   ↓
Repository
   ↓
DatabaseConnection
   ↓
Oracle Database
```

Estructura:

```text
database/
├── connection.py
├── queries.py
└── repositories/
    ├── user_repository.py
    └── account_repository.py
```

---

# 📊 Evidencia de Base de Datos

`DatabaseConnection` registra automáticamente la última operación para que `environment.py` pueda adjuntarla a Allure.

```text
SQL Query
SQL Parameters
SQL Result
```

Los steps no necesitan indicar manualmente que son de Base de Datos.

---

# 📊 Evidencia API

La misma lógica se aplica a las llamadas API.

Los steps no necesitan indicar manualmente que son de API.

El framework detecta automáticamente la evidencia generada por `ApiClient`.

---

# 📸 Screenshots y evidencia automática

La regla de evidencia es:

```text
Mobile Step
    ↓
📸 Screenshot

API Step
    ↓
🌐 API Evidence
    ↓
❌ Screenshot

Database Step
    ↓
🗄️ SQL Evidence
    ↓
❌ Screenshot
```

La detección se realiza automáticamente desde `environment.py`.

No es necesario agregar `context.step_type` a los steps.

---

# 🥒 BDD con Behave

Los escenarios se escriben utilizando Gherkin.

Ejemplo:

```gherkin
Feature: Login

    @smoke
    @login
    Scenario: Login exitoso con credenciales válidas

        Given que el usuario abre la aplicación
        When ingresa el usuario "standard_user"
        And ingresa la contraseña "secret_sauce"
        And presiona el botón LOGIN
        Then debería ingresar correctamente a la aplicación
```

---

# 🏷️ Tags

Tags principales:

```text
@smoke
@login
@api
@database
@integration
```

Ejecutar todos los escenarios `@smoke`:

```bash
behave -t @smoke
```

Ejecutar Login:

```bash
behave -t @login
```

Ejecutar API:

```bash
behave -t @api
```

Ejecutar Database:

```bash
behave -t @database
```

Ejecutar Integration:

```bash
behave -t @integration
```

---

# 📦 Instalación

## Requisitos previos

Antes de instalar el proyecto debes tener:

- Python 3.x
- Git
- Java JDK
- Node.js
- Appium Server
- Android Studio
- Android SDK
- Allure
- Dispositivo/emulador Android o iOS
- Cuenta de LambdaTest y/o BrowserStack si se requiere ejecución cloud

---

## Verificar Python

```bash
python --version
```

## Verificar Node.js

```bash
node --version
```

## Verificar npm

```bash
npm --version
```

## Verificar Java

```bash
java -version
```

## Verificar Appium

```bash
appium --version
```

## Verificar Allure

```bash
allure --version
```

---

# 🚀 Instalación del proyecto

## 1. Clonar el repositorio

```bash
git clone <REPOSITORY_URL>
cd proyecto_python
```

## 2. Crear entorno virtual

```bash
python -m venv venv
```

Activar en Git Bash:

```bash
source venv/Scripts/activate
```

CMD:

```cmd
venv\Scripts\activate
```

PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

Si agregas una nueva librería:

```bash
pip install browserstack-local
pip freeze > requirements.txt
```

---

# ⚙️ Configuración `.env`

Crear una copia de `.env.example`:

```bash
cp .env.example .env
```

Después completa las credenciales y configuración del ambiente.

Ejemplo general:

```env
# =========================================================
# EXECUTION
# =========================================================

EXECUTION_PLATFORM=local
PLATFORM_NAME=Android


# =========================================================
# LOCAL APPIUM
# =========================================================

APPIUM_SERVER=http://127.0.0.1:4723
DEVICE_NAME=emulator-5554
APP_PACKAGE=com.swaglabsmobileapp
APP_ACTIVITY=com.swaglabsmobileapp.MainActivity


# =========================================================
# LAMBDATEST
# =========================================================

LT_USERNAME=
LT_ACCESS_KEY=
LT_APP=
LT_DEVICE_INDEX=0


# =========================================================
# BROWSERSTACK
# =========================================================

BS_USERNAME=
BS_ACCESS_KEY=
BS_APP=bs://YOUR_APP_ID
BS_DEVICE_INDEX=0


# =========================================================
# BROWSERSTACK LOCAL
# =========================================================

BS_LOCAL=false
BS_LOCAL_IDENTIFIER=mobile-automation-local


# =========================================================
# API
# =========================================================

POKEMON_API_URL=https://pokeapi.co/api/v2
TEST_API_URL=https://jsonplaceholder.typicode.com
API_TIMEOUT=30


# =========================================================
# DATABASE
# =========================================================

DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=1521
DB_SERVICE=
```

---

# 🖥️ Ejecución local

Configurar:

```env
EXECUTION_PLATFORM=local
PLATFORM_NAME=Android
APPIUM_SERVER=http://127.0.0.1:4723
DEVICE_NAME=emulator-5554
APP_PACKAGE=com.swaglabsmobileapp
APP_ACTIVITY=com.swaglabsmobileapp.MainActivity
```

Iniciar Appium:

```bash
appium
```

Verificar dispositivo:

```bash
adb devices
```

Ejecutar Login:

```bash
behave -t @login -f allure_behave.formatter:AllureFormatter -o allure-results
```

---

# ☁️ Ejecución LambdaTest

Configurar:

```env
EXECUTION_PLATFORM=lambdatest
PLATFORM_NAME=Android
LT_DEVICE_INDEX=0
```

Ejecutar:

```bash
behave -t @login -f allure_behave.formatter:AllureFormatter -o allure-results
```

---

# ☁️ LambdaTest Multi-device

Configurar:

```env
EXECUTION_PLATFORM=lambdatest
PLATFORM_NAME=Android
```

Ejecutar un tag específico en todos los dispositivos configurados:

```bash
python run_devices.py @smoke
```

Otros ejemplos:

```bash
python run_devices.py @login
python run_devices.py @api
python run_devices.py @database
python run_devices.py @integration
```

Sin tag se usa `@smoke` por defecto:

```bash
python run_devices.py
```

---

# ☁️ Ejecución BrowserStack

Configurar:

```env
EXECUTION_PLATFORM=browserstack
PLATFORM_NAME=Android

BS_USERNAME=
BS_ACCESS_KEY=
BS_APP=bs://YOUR_APP_ID
BS_DEVICE_INDEX=0

BS_LOCAL=false
```

Ejecutar un escenario o tag:

```bash
behave -t @smoke -f allure_behave.formatter:AllureFormatter -o allure-results
```

---

# 🔐 BrowserStack Local + red privada

Si la aplicación o backend solo es accesible desde la red corporativa:

```env
EXECUTION_PLATFORM=browserstack
PLATFORM_NAME=Android

BS_LOCAL=true
BS_LOCAL_IDENTIFIER=mobile-automation-local
```

El framework inicia BrowserStack Local en `before_all()` y lo detiene en `after_all()`.

Para probar un solo escenario:

```bash
behave features/login.feature:4 --no-capture
```

Para probar Smoke:

```bash
behave -t @smoke --no-capture
```

La sesión BrowserStack utiliza:

```text
local=true
localIdentifier=mobile-automation-local
```

El túnel utiliza el mismo `localIdentifier`.

---

# ☁️ BrowserStack Multi-device

Configurar:

```env
EXECUTION_PLATFORM=browserstack
PLATFORM_NAME=Android
BS_LOCAL=false
```

o, si se necesita acceso a red privada:

```env
EXECUTION_PLATFORM=browserstack
PLATFORM_NAME=Android
BS_LOCAL=true
BS_LOCAL_IDENTIFIER=mobile-automation-local
```

Ejecutar todos los dispositivos configurados:

```bash
python run_devices.py @smoke
```

Ejecutar Login:

```bash
python run_devices.py @login
```

Ejecutar API:

```bash
python run_devices.py @api
```

Ejecutar Database:

```bash
python run_devices.py @database
```

Ejecutar Integration:

```bash
python run_devices.py @integration
```

El runner selecciona automáticamente `BS_DEVICE_INDEX` para cada dispositivo.

---

# 🧪 `run_test.sh`

El proyecto incluye:

```text
run_test.sh
```

Este script centraliza la ejecución de la suite.

Dar permisos:

```bash
chmod +x run_test.sh
```

Ejecutar:

```bash
./run_test.sh
```

Si la versión del script acepta un tag:

```bash
./run_test.sh @smoke
./run_test.sh @login
./run_test.sh @api
./run_test.sh @database
./run_test.sh @integration
```

---

# 📊 Allure Reports

Los resultados se almacenan en:

```text
allure-results/
```

## Limpiar resultados

```bash
rm -rf allure-results allure-report
```

## Generar y abrir reporte

```bash
allure serve allure-results
```

## Generar reporte estático

```bash
allure generate allure-results -o allure-report --clean
```

## Abrir reporte estático

```bash
allure open allure-report
```

---

# 🧪 Comandos completos recomendados

## Smoke local

```bash
rm -rf allure-results allure-report
behave -t @smoke -f allure_behave.formatter:AllureFormatter -o allure-results
allure serve allure-results
```

## Smoke LambdaTest

```bash
rm -rf allure-results allure-report
behave -t @smoke -f allure_behave.formatter:AllureFormatter -o allure-results
allure serve allure-results
```

## Smoke LambdaTest multi-device

```bash
rm -rf allure-results allure-report
python run_devices.py @smoke
allure serve allure-results
```

## Smoke BrowserStack

```bash
rm -rf allure-results allure-report
behave -t @smoke -f allure_behave.formatter:AllureFormatter -o allure-results
allure serve allure-results
```

## Smoke BrowserStack multi-device

```bash
rm -rf allure-results allure-report
python run_devices.py @smoke
allure serve allure-results
```

## BrowserStack + Local

```bash
rm -rf allure-results allure-report
behave -t @smoke --no-capture
allure serve allure-results
```

---

# 🛠️ Comandos útiles

Ver Python:

```bash
python --version
```

Ver pip:

```bash
pip --version
```

Ver dependencias:

```bash
pip list
```

Actualizar `requirements.txt`:

```bash
pip freeze > requirements.txt
```

Ver Appium:

```bash
appium --version
```

Ver dispositivos Android:

```bash
adb devices
```

Ver Allure:

```bash
allure --version
```

Ver Git:

```bash
git --version
```

---

# 🗂️ Git

```bash
git status
git add .
git commit -m "Update automation framework"
git push
```

---

# 🔐 Seguridad

Nunca subir:

```text
.env
```

El archivo `.env` puede contener:

- LambdaTest Access Key
- BrowserStack Access Key
- Usuarios
- Passwords
- API Keys
- Tokens
- Credenciales de Base de Datos

El repositorio debe contener únicamente:

```text
.env.example
```

Nunca publiques las credenciales reales en README, código, screenshots o commits.

---

# 📁 Estructura del proyecto

```text
proyecto_python/
│
├── api/
│   ├── api_client.py
│   ├── base_api.py
│   ├── endpoints.py
│   └── ...
│
├── config/
│   ├── api_config.py
│   ├── config.py
│   └── devices.py
│
├── database/
│   ├── connection.py
│   ├── queries.py
│   └── repositories/
│       ├── user_repository.py
│       └── account_repository.py
│
├── drivers/
│   └── driver_factory.py
│
├── features/
│   ├── environment.py
│   ├── steps/
│   │   ├── api_steps.py
│   │   ├── database_steps.py
│   │   └── login_steps.py
│   ├── api.feature
│   ├── database.feature
│   ├── integration.feature
│   └── login.feature
│
├── pages/
│   ├── base_page.py
│   └── login_page.py
│
├── utils/
│   ├── assertions.py
│   └── browserstack_local.py
│
├── .env
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── run_devices.py
├── run_test.sh
└── test_appium.py
```

---

# 🔄 Flujo Mobile

```text
Gherkin
   ↓
Behave
   ↓
Step Definition
   ↓
Page Object
   ↓
Driver Factory
   ↓
Local / LambdaTest / BrowserStack
   ↓
Android / iOS
```

---

# 🔄 Flujo BrowserStack Local

```text
Behave
   ↓
before_all()
   ↓
BrowserStackLocalManager
   ↓
BrowserStack Local
   ↓
BrowserStack Device
   ↓
VPN / Red corporativa
   ↓
Backend interno
   ↓
after_all()
```

---

# 🔄 Flujo API

```text
Gherkin
   ↓
Behave
   ↓
API Step
   ↓
API Class
   ↓
BaseApi
   ↓
ApiClient
   ↓
REST API
```

---

# 🔄 Flujo Database

```text
Gherkin
   ↓
Behave
   ↓
Database Step
   ↓
Repository
   ↓
DatabaseConnection
   ↓
Oracle
```

---

# 🧩 Principios del Framework

## Separación de responsabilidades

```text
Pages
   ↓
Mobile UI

API Classes
   ↓
Business API Operations

ApiClient
   ↓
HTTP Communication

Repositories
   ↓
Database Operations

Driver Factory
   ↓
Mobile Execution

Environment
   ↓
Framework Lifecycle

Allure
   ↓
Evidence / Reporting
```

## Reutilización

La lógica común se centraliza en:

```text
BasePage
BaseApi
ApiClient
DatabaseConnection
Driver Factory
```

## Configuración externa

La configuración dependiente del ambiente se mantiene en:

```text
.env
```

Esto permite cambiar entre Local, LambdaTest y BrowserStack sin modificar los escenarios.

---

# 🌎 Ambientes

El framework puede configurarse mediante variables de entorno para diferentes ambientes:

```text
DEV
QA
UAT
```

Las URLs, credenciales y configuraciones dependientes del ambiente se mantienen fuera del código fuente.

---

# 📋 Checklist de instalación

```text
[ ] Instalar Python
[ ] Instalar Git
[ ] Instalar Node.js
[ ] Instalar Java
[ ] Instalar Appium
[ ] Instalar Allure
[ ] Configurar Android SDK
[ ] Crear entorno virtual
[ ] Activar entorno virtual
[ ] Instalar requirements.txt
[ ] Instalar browserstack-local si se utilizará BrowserStack Local
[ ] Crear .env desde .env.example
[ ] Configurar Appium, LambdaTest o BrowserStack
[ ] Configurar BrowserStack Local si aplica
[ ] Configurar Base de Datos
[ ] Verificar dispositivo
[ ] Ejecutar prueba Login
[ ] Ejecutar prueba API
[ ] Ejecutar prueba Database
[ ] Generar reporte Allure
```

---

# ⚡ Quick Start

```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
cp .env.example .env
```

Configura `EXECUTION_PLATFORM`:

```env
EXECUTION_PLATFORM=local
```

```env
EXECUTION_PLATFORM=lambdatest
```

```env
EXECUTION_PLATFORM=browserstack
```

Para BrowserStack Local:

```env
BS_LOCAL=true
BS_LOCAL_IDENTIFIER=mobile-automation-local
```

Ejecutar una suite:

```bash
./run_test.sh
```

Ejecutar multi-device:

```bash
python run_devices.py @smoke
```

Abrir reporte:

```bash
allure serve allure-results
```

---

# 📌 Roadmap

```text
[x] Python + Behave
[x] Appium
[x] Android
[x] iOS
[x] Ejecución local
[x] LambdaTest
[x] LambdaTest Multi-device
[x] BrowserStack
[x] BrowserStack Multi-device
[x] BrowserStack Local
[x] Allure
[x] API Automation
[x] GET
[x] POST
[x] PUT
[x] DELETE
[x] Oracle Database
[x] Repository Pattern
[x] API Evidence
[x] Database Evidence
[x] Mobile Screenshots
[x] .env Configuration
[x] Multiple API Domains
[x] Tags dinámicos en run_devices.py
[x] Allure agrupado por proveedor/dispositivo

[ ] PATCH
[ ] Authentication
[ ] CI/CD
[ ] Parallel Execution
[ ] GitHub Actions
```

---

# 👨‍💻 Autor

QA Automation Framework desarrollado en Python para automatización:

- Mobile
- API
- Database
- Integration Testing
- Cloud Device Testing

---

# 📄 License

Este proyecto es utilizado con fines de automatización y aprendizaje.
