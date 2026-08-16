# 📱 Mobile Automation Framework - Python

Framework de automatización de pruebas desarrollado en **Python**, utilizando **Behave, Appium, Requests, Oracle Database, LambdaTest y Allure Reports**.

El framework permite automatizar y validar diferentes capas de una aplicación:

- 📱 Automatización Mobile
- 🌐 Automatización de APIs REST
- 🗄️ Automatización de Base de Datos Oracle
- 🔗 Pruebas de integración Mobile + API + Database
- ☁️ Ejecución en dispositivos reales mediante LambdaTest
- 📱 Ejecución en múltiples dispositivos
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
- Ejecución en LambdaTest
- Emuladores
- Dispositivos reales
- Ejecución en múltiples dispositivos
- Captura automática de screenshots
- Page Object Model

---

## 🌐 API Automation

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

Las llamadas API generan automáticamente evidencia para Allure:

- API
- HTTP Method
- Endpoint
- Parameters
- Headers
- Body
- Status Code
- Response

---

## 🗄️ Database Automation

Integración con Oracle Database utilizando `oracledb`.

Permite ejecutar:

- SELECT
- INSERT
- UPDATE
- DELETE

La arquitectura utiliza Repository Pattern:

```text
Test Steps
    ↓
Repository
    ↓
Database Connection
    ↓
Oracle Database
```

También se genera evidencia de:

- SQL Query
- SQL Parameters
- SQL Result

---

## 🔗 Integration Testing

El framework permite combinar diferentes capas dentro de un mismo escenario.

Ejemplo:

```text
Mobile
   ↓
API
   ↓
Database
```

Esto permite validar flujos completos de negocio.

---

# 🛠️ Tecnologías

| Tecnología | Uso |
|---|---|
| Python | Lenguaje principal |
| Behave | BDD / Gherkin |
| Appium | Automatización Mobile |
| UiAutomator2 | Automatización Android |
| XCUITest | Automatización iOS |
| LambdaTest | Dispositivos reales en la nube |
| Requests | Automatización API |
| OracleDB | Automatización de Base de Datos |
| python-dotenv | Variables de entorno |
| Allure | Reportes |
| Git | Control de versiones |

---

# 📁 Estructura del proyecto

```text
proyecto_python/
│
├── api/
│   ├── api_client.py
│   ├── base_api.py
│   ├── endpoints.py
│   ├── pokemon_api.py
│   └── test_api.py
│
├── config/
│   ├── api_config.py
│   ├── config.py
│   └── devices.py
│
├── database/
│   ├── connection.py
│   ├── queries.py
│   │
│   └── repositories/
│       ├── user_repository.py
│       └── account_repository.py
│
├── drivers/
│   └── driver_factory.py
│
├── features/
│   ├── environment.py
│   │
│   ├── steps/
│   │   ├── api_steps.py
│   │   ├── database_steps.py
│   │   └── login_steps.py
│   │
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
│   └── assertions.py
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

# 🏗️ Arquitectura

El framework está dividido en diferentes capas para mantener una correcta separación de responsabilidades.

```text
                         Behave
                           │
                           ▼
                     Gherkin Tests
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
          Mobile          API            DB
             │             │             │
             ▼             ▼             ▼
          Appium        ApiClient      Repository
             │             │             │
             ▼             ▼             ▼
        Android/iOS     REST APIs      Oracle
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                         Allure
```

---

# 📱 Arquitectura Mobile

La creación del driver está centralizada en:

```text
drivers/driver_factory.py
```

El Driver Factory permite seleccionar automáticamente el entorno de ejecución.

```text
                    Driver Factory
                         │
              ┌──────────┴──────────┐
              │                     │
            LOCAL               LAMBDATEST
              │                     │
         ┌────┴────┐          ┌─────┴─────┐
         │         │          │           │
      Android     iOS      Android       iOS
```

La plataforma se determina mediante:

```env
EXECUTION_PLATFORM=local
PLATFORM_NAME=Android
```

o:

```env
EXECUTION_PLATFORM=lambdatest
PLATFORM_NAME=Android
```

---

# ☁️ LambdaTest

El framework permite ejecutar pruebas en dispositivos reales mediante LambdaTest.

Configuración:

```env
EXECUTION_PLATFORM=lambdatest

PLATFORM_NAME=Android

LT_USERNAME=

LT_ACCESS_KEY=

LT_APP=

LT_DEVICE_INDEX=0
```

Las credenciales deben mantenerse únicamente en `.env`.

---

# 📱 Configuración de dispositivos

Los dispositivos disponibles se mantienen en:

```text
config/devices.py
```

Ejemplo:

```python
ANDROID_DEVICES = [

    {
        "name": "Galaxy S23",
        "platform_version": "14"
    },

    {
        "name": "Pixel 10 Pro",
        "platform_version": "16"
    }
]
```

Para iOS:

```python
IOS_DEVICES = [

    {
        "name": "iPhone 15",
        "platform_version": "17"
    }
]
```

El dispositivo se selecciona utilizando:

```env
LT_DEVICE_INDEX=0
```

---

# 📱 Ejecución en múltiples dispositivos

El proyecto incluye:

```text
run_devices.py
```

Este script permite ejecutar los escenarios configurados sobre diferentes dispositivos.

Ejecutar:

```bash
python run_devices.py
```

El flujo es:

```text
Device 1
   ↓
LambdaTest
   ↓
Behave
   ↓
Allure Results

Device 2
   ↓
LambdaTest
   ↓
Behave
   ↓
Allure Results

Device 3
   ↓
LambdaTest
   ↓
Behave
   ↓
Allure Results
```

La información del dispositivo se incorpora al reporte de Allure.

---

# 🌐 Arquitectura API

La capa API está organizada de la siguiente manera:

```text
api/
│
├── api_client.py
├── base_api.py
├── endpoints.py
├── pokemon_api.py
└── test_api.py
```

---

# ApiClient

`api_client.py` contiene la lógica HTTP común.

Es responsable de ejecutar:

```text
GET
POST
PUT
DELETE
```

El `ApiClient` centraliza la comunicación HTTP y la evidencia de las llamadas.

---

# BaseApi

`base_api.py` proporciona una clase base para las diferentes APIs.

Ejemplo:

```python
from api.base_api import BaseApi


class TransferApi(BaseApi):

    def create_transfer(
        self,
        body,
        headers=None
    ):

        return self.api_client.post(
            "/transfers",
            body=body,
            headers=headers
        )
```

Las clases específicas solamente definen las operaciones de negocio.

---

# Endpoints

Los endpoints pueden centralizarse en:

```text
api/endpoints.py
```

Ejemplo:

```python
class Endpoints:

    POKEMON = "/pokemon"

    POSTS = "/posts"

    LOGIN = "/login"

    TRANSFERS = "/transfers"

    QR = "/qr"
```

Esto permite mantener las rutas organizadas y evitar duplicación.

---

# 🌍 Múltiples APIs / Dominios

El framework permite trabajar con diferentes dominios.

Por ejemplo:

```text
Auth API
https://auth-api.com

Transfer API
https://transfer-api.com

QR API
https://qr-api.com
```

Las URLs se configuran mediante `.env`.

Ejemplo:

```env
AUTH_API_URL=
TRANSFER_API_URL=
QR_API_URL=
```

Y se recuperan desde:

```text
config/api_config.py
```

Cada dominio puede tener su propia clase:

```text
api/
├── auth_api.py
├── transfer_api.py
└── qr_api.py
```

Cada clase reutiliza el mismo `ApiClient`.

---

# ⚙️ Configuración de APIs

Archivo:

```text
config/api_config.py
```

Ejemplo:

```python
import os

from dotenv import load_dotenv


load_dotenv()


POKEMON_API_URL = os.getenv(
    "POKEMON_API_URL"
)

TEST_API_URL = os.getenv(
    "TEST_API_URL"
)

API_TIMEOUT = int(
    os.getenv(
        "API_TIMEOUT",
        "30"
    )
)
```

Las URLs reales se mantienen en `.env`.

---

# 📡 Ejemplo GET

```python
response = context.pokemon_api.get_pokemon(
    "pikachu"
)
```

---

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

---

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

---

# 📡 Ejemplo DELETE

```python
response = context.test_api.delete_user(
    user_id=1
)
```

---

# 🗄️ Arquitectura Database

La capa de Base de Datos utiliza Repository Pattern.

```text
features/steps
       ↓
Repository
       ↓
DatabaseConnection
       ↓
Oracle
```

Estructura:

```text
database/
│
├── connection.py
├── queries.py
│
└── repositories/
    ├── user_repository.py
    └── account_repository.py
```

---

# 🔌 DatabaseConnection

Archivo:

```text
database/connection.py
```

Responsabilidades:

- Crear conexión Oracle
- Ejecutar SELECT
- Ejecutar INSERT
- Ejecutar UPDATE
- Ejecutar DELETE
- Commit
- Rollback
- Cerrar conexión
- Registrar evidencia

---

# 🔎 SELECT

Ejemplo:

```python
account = (
    context.account_repository.get_account(
        id_cuenta
    )
)
```

---

# ✏️ UPDATE

Ejemplo:

```python
context.account_repository.update_account(
    id_cuenta=id_cuenta,
    saldo=saldo
)
```

---

# 🗑️ DELETE

Las operaciones DELETE utilizan el mismo mecanismo de ejecución de operaciones de modificación.

Ejemplo:

```python
context.user_repository.delete_user(
    id_usuario
)
```

---

# 📊 Evidencia Database

Allure puede mostrar:

```text
SQL Query
SQL Parameters
SQL Result
```

Esto permite conocer exactamente qué operación se ejecutó durante el escenario.

---

# 🥒 BDD con Behave

Los escenarios se escriben utilizando Gherkin.

Ejemplo:

```gherkin
Feature: Login

    @smoke
    Scenario: Login fallido con credenciales inválidas

        Given que el usuario abre la aplicación

        When ingresa el usuario "invalid_user"

        And ingresa la contraseña "invalid_password"

        And presiona el botón LOGIN

        Then debería mostrar un mensaje de error
```

---

# 🏷️ Tags

El framework utiliza tags para ejecutar diferentes grupos de pruebas.

Ejemplos:

```text
@smoke
@login
@api
@database
@integration
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
- Un dispositivo Android/iOS o acceso a LambdaTest

---

## Verificar Python

```bash
python --version
```

---

## Verificar Node.js

```bash
node --version
```

---

## Verificar npm

```bash
npm --version
```

---

## Verificar Java

```bash
java -version
```

---

## Verificar Appium

```bash
appium --version
```

---

## Verificar Allure

```bash
allure --version
```

---

# 🚀 Instalación del proyecto

## 1. Clonar el repositorio

```bash
git clone <REPOSITORY_URL>
```

Ingresar al proyecto:

```bash
cd proyecto_python
```

---

# 2. Crear entorno virtual

Windows:

```bash
python -m venv venv
```

Activar en Git Bash:

```bash
source venv/Scripts/activate
```

Activar en CMD:

```cmd
venv\Scripts\activate
```

Activar en PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

Una vez activado debería aparecer:

```text
(venv)
```

al inicio de la terminal.

---

# 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

Verificar:

```bash
pip list
```

---

# ⚙️ Configuración

## 4. Crear archivo `.env`

El proyecto incluye:

```text
.env.example
```

Crear una copia:

```bash
cp .env.example .env
```

Luego completar las variables necesarias.

---

# 📄 Variables de entorno

Ejemplo:

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

# 📱 Configuración Mobile Local

Para ejecutar Appium localmente:

```env
EXECUTION_PLATFORM=local

PLATFORM_NAME=Android

APPIUM_SERVER=http://127.0.0.1:4723

DEVICE_NAME=emulator-5554

APP_PACKAGE=com.swaglabsmobileapp

APP_ACTIVITY=com.swaglabsmobileapp.MainActivity
```

---

# 🔌 Verificar dispositivo Android

```bash
adb devices
```

Ejemplo:

```text
List of devices attached
emulator-5554    device
```

---

# ▶️ Iniciar Appium

```bash
appium
```

Por defecto:

```text
http://127.0.0.1:4723
```

---

# ☁️ Configuración LambdaTest

Para ejecutar en LambdaTest:

```env
EXECUTION_PLATFORM=lambdatest

PLATFORM_NAME=Android

LT_USERNAME=

LT_ACCESS_KEY=

LT_APP=

LT_DEVICE_INDEX=0
```

---

# ▶️ Ejecución de pruebas

El framework permite ejecutar las pruebas:

- Localmente mediante Appium
- En LambdaTest
- En múltiples dispositivos
- Por tags
- Por feature
- Por escenario específico

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
behave -t @login \
-f allure_behave.formatter:AllureFormatter \
-o allure-results
```

---

# ☁️ Ejecución en LambdaTest

Configurar:

```env
EXECUTION_PLATFORM=lambdatest

PLATFORM_NAME=Android

LT_USERNAME=YOUR_USERNAME

LT_ACCESS_KEY=YOUR_ACCESS_KEY

LT_APP=lt://YOUR_APP_ID

LT_DEVICE_INDEX=0
```

Luego ejecutar:

```bash
behave -t @login \
-f allure_behave.formatter:AllureFormatter \
-o allure-results
```

El `driver_factory.py` detectará:

```env
EXECUTION_PLATFORM=lambdatest
```

y creará automáticamente el driver remoto de LambdaTest.

---

# 📱 Ejecutar múltiples dispositivos en LambdaTest

Configurar:

```env
EXECUTION_PLATFORM=lambdatest

PLATFORM_NAME=Android
```

Luego ejecutar:

```bash
python run_devices.py
```

El script utiliza los dispositivos configurados en:

```text
config/devices.py
```

Cada ejecución se realiza sobre un dispositivo diferente.

---

# 🧪 run_test.sh

El proyecto incluye:

```text
run_test.sh
```

Este script permite centralizar la ejecución de las pruebas.

Ejemplo:

```bash
#!/bin/bash

echo "================================="
echo "   MOBILE AUTOMATION FRAMEWORK"
echo "================================="

echo ""
echo "Limpiando resultados anteriores..."

rm -rf allure-results allure-report

echo ""
echo "Ejecutando pruebas..."

behave \
-f allure_behave.formatter:AllureFormatter \
-o allure-results

echo ""
echo "================================="
echo "       EJECUCIÓN FINALIZADA"
echo "================================="
```

---

# ▶️ Dar permisos a run_test.sh

```bash
chmod +x run_test.sh
```

Ejecutar:

```bash
./run_test.sh
```

---

# 🧪 Ejecutar un tag mediante run_test.sh

Si el script está configurado para recibir un tag:

```bash
./run_test.sh @login
```

Ejemplo API:

```bash
./run_test.sh @api
```

Database:

```bash
./run_test.sh @database
```

Integration:

```bash
./run_test.sh @integration
```

---

# 🌐 Ejecutar API

Todos los escenarios API:

```bash
behave -t @api \
-f allure_behave.formatter:AllureFormatter \
-o allure-results
```

---

## Ejecutar Feature API

```bash
behave features/api.feature \
-f allure_behave.formatter:AllureFormatter \
-o allure-results
```

---

## Ejecutar escenario API específico

```bash
behave features/api.feature \
-n "Crear un post mediante API" \
-f allure_behave.formatter:AllureFormatter \
-o allure-results
```

---

# 🗄️ Ejecutar Database

```bash
behave -t @database \
-f allure_behave.formatter:AllureFormatter \
-o allure-results
```

---

# 🔗 Ejecutar Integration

```bash
behave -t @integration \
-f allure_behave.formatter:AllureFormatter \
-o allure-results
```

---

# 📱 Ejecutar Mobile

## Login

```bash
behave -t @login \
-f allure_behave.formatter:AllureFormatter \
-o allure-results
```

---

## Smoke

```bash
behave -t @smoke \
-f allure_behave.formatter:AllureFormatter \
-o allure-results
```

---

## Feature específico

```bash
behave features/login.feature \
-f allure_behave.formatter:AllureFormatter \
-o allure-results
```

---

## Escenario específico

```bash
behave features/login.feature \
-n "Login fallido con credenciales inválidas" \
-f allure_behave.formatter:AllureFormatter \
-o allure-results
```

---

# 🏷️ Ejecución por Tags

## Login

```bash
behave -t @login
```

## Smoke

```bash
behave -t @smoke
```

## API

```bash
behave -t @api
```

## Database

```bash
behave -t @database
```

## Integration

```bash
behave -t @integration
```

---

# 📊 Allure Reports

Los resultados de Allure se almacenan en:

```text
allure-results/
```

---

# 🧹 Limpiar resultados anteriores

Antes de una nueva ejecución:

```bash
rm -rf allure-results allure-report
```

---

# 📈 Abrir reporte Allure

Después de ejecutar las pruebas:

```bash
allure serve allure-results
```

Esto genera y abre automáticamente el reporte en el navegador.

---

# 📦 Generar reporte estático

```bash
allure generate allure-results \
-o allure-report \
--clean
```

Abrir:

```bash
allure open allure-report
```

---

# 🔄 Flujo recomendado de ejecución

## Ejecución local

### 1. Activar entorno virtual

```bash
source venv/Scripts/activate
```

### 2. Iniciar Appium

```bash
appium
```

### 3. Limpiar resultados

```bash
rm -rf allure-results allure-report
```

### 4. Ejecutar pruebas

```bash
behave -t @login \
-f allure_behave.formatter:AllureFormatter \
-o allure-results
```

### 5. Abrir Allure

```bash
allure serve allure-results
```

---

# 🔄 Ejecución LambdaTest

### 1. Configurar `.env`

```env
EXECUTION_PLATFORM=lambdatest
PLATFORM_NAME=Android
LT_DEVICE_INDEX=0
```

### 2. Limpiar resultados

```bash
rm -rf allure-results allure-report
```

### 3. Ejecutar pruebas

```bash
behave -t @login \
-f allure_behave.formatter:AllureFormatter \
-o allure-results
```

### 4. Abrir Allure

```bash
allure serve allure-results
```

---

# 🔄 Ejecución LambdaTest Multi-Device

### 1. Configurar:

```env
EXECUTION_PLATFORM=lambdatest
PLATFORM_NAME=Android
```

### 2. Limpiar resultados:

```bash
rm -rf allure-results allure-report
```

### 3. Ejecutar:

```bash
python run_devices.py
```

### 4. Abrir Allure:

```bash
allure serve allure-results
```

---

# 🌐 Ejecución API completa

```bash
rm -rf allure-results allure-report

behave -t @api \
-f allure_behave.formatter:AllureFormatter \
-o allure-results

allure serve allure-results
```

---

# 🗄️ Ejecución Database completa

```bash
rm -rf allure-results allure-report

behave -t @database \
-f allure_behave.formatter:AllureFormatter \
-o allure-results

allure serve allure-results
```

---

# 🔗 Ejecución Integration completa

```bash
rm -rf allure-results allure-report

behave -t @integration \
-f allure_behave.formatter:AllureFormatter \
-o allure-results

allure serve allure-results
```

---

# 🧪 Ejecución de todas las pruebas

```bash
rm -rf allure-results allure-report

behave \
-f allure_behave.formatter:AllureFormatter \
-o allure-results

allure serve allure-results
```

---

# 🛠️ Comandos útiles

## Ver versión de Python

```bash
python --version
```

## Ver versión de pip

```bash
pip --version
```

## Ver dependencias instaladas

```bash
pip list
```

## Actualizar requirements.txt

```bash
pip freeze > requirements.txt
```

## Ver versión de Appium

```bash
appium --version
```

## Ver dispositivos Android

```bash
adb devices
```

## Ver versión de Allure

```bash
allure --version
```

## Ver versión de Git

```bash
git --version
```

---

# 🗂️ Comandos Git

## Ver estado

```bash
git status
```

## Agregar cambios

```bash
git add .
```

## Crear commit

```bash
git commit -m "Update automation framework"
```

## Subir cambios

```bash
git push
```

---

# 🔐 Seguridad

Nunca subir el archivo:

```text
.env
```

El archivo `.env` puede contener información sensible como:

- LambdaTest Access Key
- LambdaTest Username
- Database Username
- Database Password
- API Keys
- Tokens
- Credenciales de ambientes

El repositorio debe contener:

```text
.env.example
```

pero no:

```text
.env
```

---

# 📝 .env.example

El archivo `.env.example` sirve como plantilla para configurar el proyecto.

Ejemplo:

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

DEVICE_NAME=Android

APP_PACKAGE=

APP_ACTIVITY=


# =========================================================
# LAMBDATEST
# =========================================================

LT_USERNAME=

LT_ACCESS_KEY=

LT_APP=

LT_DEVICE_INDEX=0


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

No debe contener:

- Passwords reales
- Access Keys
- Tokens
- API Keys
- Credenciales de Base de Datos

---

# 📸 Evidencia Allure

El framework genera evidencia automáticamente.

## Mobile

```text
Screenshot
Device
Platform
Version
Execution
```

## API

```text
API Method
API Endpoint
API Parameters
API Headers
API Body
API Status Code
API Response
```

## Database

```text
SQL Query
SQL Parameters
SQL Result
```

## Assertions

```text
Assertion
Expected
Actual
```

---

# 📸 Screenshots

Los screenshots Mobile se capturan automáticamente durante los Steps y se adjuntan a Allure.

Ejemplo:

```text
Screenshot - que el usuario abre la aplicación

Screenshot - ingresa el usuario

Screenshot - ingresa la contraseña

Screenshot - presiona el botón LOGIN

Screenshot - debería mostrar un mensaje de error
```

Los Steps de API y Database no generan screenshots de Appium.

---

# 🔎 Assertions

Las validaciones se centralizan mediante:

```text
utils/assertions.py
```

Ejemplo:

```python
verify(
    context,
    actual=actual,
    expected=expected,
    description="API Status Code"
)
```

Allure registra:

```text
Assertion
Expected
Actual
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
Appium
   ↓
Android / iOS
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

# 🔗 Flujo de integración

```text
                ┌─────────────┐
                │   Behave    │
                └──────┬──────┘
                       │
                       ▼
                ┌─────────────┐
                │    Mobile   │
                └──────┬──────┘
                       │
                       ▼
                ┌─────────────┐
                │     API     │
                └──────┬──────┘
                       │
                       ▼
                ┌─────────────┐
                │  Database   │
                └──────┬──────┘
                       │
                       ▼
                ┌─────────────┐
                │   Allure    │
                └─────────────┘
```

---

# 🧩 Principios del Framework

## Separación de responsabilidades

Cada capa tiene una responsabilidad específica:

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

---

## Reutilización

La lógica común se centraliza en:

```text
BasePage
BaseApi
ApiClient
DatabaseConnection
```

Esto evita duplicación de código.

---

## Configuración externa

La configuración dependiente del ambiente se mantiene en:

```text
.env
```

Esto permite cambiar entre ambientes sin modificar los Steps.

---

# 🌎 Ambientes

El framework puede configurarse para diferentes ambientes mediante variables de entorno.

Ejemplo:

```text
DEV
QA
UAT
```

Las URLs, credenciales y configuraciones dependientes del ambiente se mantienen fuera del código fuente.

---

# 📋 Checklist de instalación

Después de clonar el proyecto:

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
[ ] Crear .env desde .env.example
[ ] Configurar Appium o LambdaTest
[ ] Configurar Base de Datos
[ ] Verificar dispositivo
[ ] Ejecutar prueba Login
[ ] Ejecutar prueba API
[ ] Ejecutar prueba Database
[ ] Generar reporte Allure
```

---

# ⚡ Quick Start

Después de tener todas las dependencias instaladas:

```bash
python -m venv venv
```

```bash
source venv/Scripts/activate
```

```bash
pip install -r requirements.txt
```

Crear `.env`:

```bash
cp .env.example .env
```

Configurar las variables necesarias.

Para ejecución local:

```env
EXECUTION_PLATFORM=local
```

Para LambdaTest:

```env
EXECUTION_PLATFORM=lambdatest
```

Ejecutar:

```bash
./run_test.sh
```

Para múltiples dispositivos:

```bash
python run_devices.py
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
[x] LambdaTest
[x] Multi-device
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

[ ] PATCH
[ ] Authentication
[ ] CI/CD
[ ] Parallel Execution
[ ] BrowserStack
```

---

# 👨‍💻 Autor

QA Automation Framework desarrollado en Python para automatización:

- Mobile
- API
- Database
- Integration Testing

---

# 📄 License

Este proyecto es utilizado con fines de automatización y aprendizaje.