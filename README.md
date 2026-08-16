# 📱 Mobile Automation Framework

Framework de automatización de pruebas móviles desarrollado con **Python, Appium, Behave, Gherkin y Allure**, utilizando **Page Object Model (POM)** para la automatización Mobile e incorporando integración con **APIs REST y Oracle Database**.

El objetivo del framework es permitir la ejecución de pruebas funcionales e integradas, manteniendo separadas las responsabilidades de **Frontend, API, Base de Datos y Assertions**, y generando evidencia detallada por cada Step.

---

## 🎯 Objetivos

El framework permite automatizar y validar:

- 📱 Flujos de aplicaciones Android.
- 🌐 Consumo y validación de APIs REST.
- 🗄️ Consultas y validaciones contra Oracle Database.
- 🔎 Assertions reutilizables con Expected / Actual.
- 📸 Screenshots por Step de Front.
- 📊 Evidencias detalladas en Allure.
- 🔄 Precondiciones mediante `Background`.
- 🔗 Escenarios combinando Front + API + Base de Datos.

---

# 🛠️ Tecnologías

| Tecnología | Uso |
|---|---|
| Python | Lenguaje principal |
| Appium | Automatización Mobile |
| UiAutomator2 | Driver Android |
| Behave | Framework BDD |
| Gherkin | Definición de escenarios |
| Selenium | WebDriver y esperas explícitas |
| Requests | Consumo de APIs REST |
| Oracle / oracledb | Integración con Base de Datos |
| python-dotenv | Variables de entorno |
| Allure | Reportería y evidencias |
| ADB | Comunicación con dispositivos Android |
| Android Studio | Android SDK y Emulator |
| Appium Inspector | Identificación de elementos |
| Git / GitHub | Control de versiones |

---

# 🏗️ Arquitectura

El framework utiliza diferentes capas para separar responsabilidades.

```text
                         GHERKIN
                            │
                          BEHAVE
                            │
                      STEP DEFINITIONS
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
     PAGE OBJECTS        API LAYER         DB LAYER
          │                 │                 │
          ▼                 ▼                 ▼
        Appium           ApiClient       Repository
          │                 │                 │
          ▼                 ▼                 ▼
      Android            REST API          Oracle
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
                            ▼
                       ASSERTIONS
                            │
                            ▼
                          ALLURE
```

### Principio principal

Los Steps describen **qué se quiere validar**.

Las diferentes capas se encargan de **cómo realizarlo**.

Ejemplo:

```python
context.login_page.enter_username(username)
```

El Step no necesita conocer cómo Appium encuentra el elemento.

---

# 📂 Estructura del proyecto

```text
proyecto__python/
│
├── app/
│   └── application.apk
│
├── api/
│   ├── api_client.py
│   └── pokemon_api.py
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
├── pages/
│   ├── base_page.py
│   └── login_page.py
│
├── utils/
│   └── assertions.py
│
├── config/
│   └── config.py
│
├── test_data/
│
├── features/
│   ├── environment.py
│   ├── login.feature
│   ├── api.feature
│   ├── database.feature
│   ├── integration.feature
│   │
│   └── steps/
│       ├── login_steps.py
│       ├── api_steps.py
│       └── database_steps.py
│
├── screenshots/
├── allure-results/
├── allure-report/
│
├── .env
├── .gitignore
├── requirements.txt
├── run_tests.sh
└── README.md
```

> `venv/`, `.env`, `screenshots/`, `allure-results/` y `allure-report/` no deben subirse al repositorio.

---

# 📁 Componentes principales

## `features/`

Contiene los escenarios escritos en Gherkin.

Ejemplo:

```gherkin
Feature: Login

    Scenario: Login exitoso con credenciales válidas

        Given que el usuario abre la aplicación

        When ingresa el usuario "standard_user"
        And ingresa la contraseña "secret_sauce"
        And presiona el botón LOGIN

        Then debería ingresar correctamente a la aplicación
```

---

## `features/steps/`

Contiene la implementación Python de los Steps.

Ejemplo:

```python
@when('ingresa el usuario "{username}"')
def step_enter_username(context, username):

    context.login_page.enter_username(username)
```

Los Steps deben mantenerse simples y delegar la lógica a Page Objects, APIs o Repositories.

---

# 📱 Mobile Automation

## `pages/`

Contiene los Page Objects de la aplicación.

Ejemplo:

```text
pages/
├── base_page.py
├── login_page.py
└── home_page.py
```

Cada Page Object contiene:

- Locators.
- Acciones de la pantalla.
- Métodos reutilizables.

---

## `pages/base_page.py`

Contiene acciones comunes:

```python
class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def find_element(self, locator):
        return self.wait.until(
            EC.presence_of_element_located(locator)
        )

    def click(self, locator):
        element = self.wait.until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def enter_text(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.find_element(locator).text
```

Se utilizan **esperas explícitas** para evitar depender de `time.sleep()`.

---

# 🔍 Locators

Siempre que sea posible, utilizar locators estables.

Preferencia:

```python
AppiumBy.ACCESSIBILITY_ID
```

antes que XPath.

Ejemplo:

```python
USERNAME = (
    AppiumBy.ACCESSIBILITY_ID,
    "test-Username"
)
```

Cuando no exista un locator estable, puede utilizarse XPath:

```python
(
    AppiumBy.XPATH,
    '//android.widget.TextView[@text="PRODUCTS"]'
)
```

---

# 🚗 Driver de Appium

`drivers/driver_factory.py` centraliza la creación del driver.

Ejemplo:

```python
from appium import webdriver
from appium.options.android import UiAutomator2Options


def create_driver():

    options = UiAutomator2Options()

    options.platform_name = "Android"
    options.device_name = "emulator-5554"
    options.automation_name = "UiAutomator2"

    options.app_package = "com.example.app"
    options.app_activity = ".MainActivity"

    options.app_wait_activity = "*"
    options.new_command_timeout = 120

    driver = webdriver.Remote(
        "http://127.0.0.1:4723",
        options=options
    )

    return driver
```

Los valores de Package, Activity, dispositivo y servidor deben adaptarse al ambiente.

---

# 🌐 API Automation

La capa API está separada en dos niveles:

```text
Step
 ↓
PokemonApi
 ↓
ApiClient
 ↓
Requests
 ↓
REST API
```

## `api/api_client.py`

El `ApiClient` centraliza las llamadas HTTP.

Ejemplo:

```python
import requests


class ApiClient:

    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint, params=None, headers=None):

        url = f"{self.base_url}{endpoint}"

        response = requests.get(
            url,
            params=params,
            headers=headers
        )

        return response
```

## API específica

Ejemplo:

```python
class PokemonApi:

    def __init__(self, api_client):
        self.api_client = api_client

    def get_pokemon(self, pokemon):

        return self.api_client.get(
            f"/pokemon/{pokemon}"
        )
```

Esto permite cambiar o ampliar APIs sin modificar los Steps.

---

# 🗄️ Database Automation

La integración con Base de Datos utiliza:

```text
Step
 ↓
Repository
 ↓
DatabaseConnection
 ↓
Oracle
```

La conexión se encuentra en:

```text
database/connection.py
```

Las queries se centralizan en:

```text
database/queries.py
```

Los repositories encapsulan el acceso:

```text
database/repositories/
├── user_repository.py
└── account_repository.py
```

---

## Queries

Ejemplo:

```python
class Queries:

    GET_USER = """
        SELECT
            id_usuario,
            usuario,
            nombre
        FROM usuarios
    """
```

---

## Repository

Ejemplo:

```python
from database.queries import Queries


class UserRepository:

    def __init__(self, db):
        self.db = db

    def get_users(self):

        return self.db.execute_query(
            Queries.GET_USER
        )
```

El Step solamente consume el Repository:

```python
users = context.user_repository.get_users()
```

De esta forma, el Step no necesita conocer SQL ni la implementación de conexión.

---

# 🔎 Assertions

Las validaciones utilizan una función reutilizable:

```python
verify(
    context,
    actual=actual,
    expected=expected,
    description="Descripción"
)
```

Ejemplo:

```python
verify(
    context,
    actual=context.response.status_code,
    expected=200,
    description="API Status Code"
)
```

La evidencia generada incluye:

```text
Assertion
Expected
Actual
```

La evidencia se registra antes del `assert`, permitiendo mostrar Expected / Actual incluso cuando la validación falla.

---

# 📸 Sistema de evidencias

Una de las características principales del framework es la generación de evidencia por Step.

## 📱 Front / Appium

Los Steps que interactúan con la aplicación generan:

```text
📎 Screenshot
```

Ejemplo:

```text
When ingresa el usuario "standard_user"

    📎 Screenshot - ingresa el usuario
```

---

## 🌐 API

Los Steps que realizan llamadas API generan:

```text
📎 API Method
📎 API Endpoint
📎 API Parameters
📎 API Status Code
📎 API Response
```

Ejemplo:

```text
Method:
GET

Endpoint:
https://pokeapi.co/api/v2/pokemon/pikachu

Status Code:
200

Response:
{
    "id": 25,
    "name": "pikachu"
}
```

---

## 🗄️ Database

Los Steps que ejecutan consultas generan:

```text
📎 SQL Query
📎 SQL Parameters
📎 SQL Result
```

Ejemplo:

```text
SQL Query:

SELECT id_usuario,
       usuario,
       nombre
FROM usuarios

Parameters:
{}

Result:
[(1, 'standard_user', 'Standard User')]
```

---

## 🔎 Assertions

Las validaciones generan:

```text
📎 Assertion
📎 Expected
📎 Actual
```

Ejemplo:

```text
Assertion:
API Status Code

Expected:
200

Actual:
200
```

---

# 📊 Allure Report

Allure permite visualizar la ejecución y las evidencias de cada Step.

El resultado de Behave se almacena en:

```text
allure-results/
```

El reporte generado puede almacenarse en:

```text
allure-report/
```

---

# ❌ Failed vs Broken

El framework diferencia entre fallos funcionales y errores técnicos.

## 🔴 Failed

Se utiliza cuando una validación funcional no cumple.

Ejemplo:

```text
Expected:
PRODUCTS

Actual:
PRODUCTS no encontrado
```

Esto representa un fallo funcional.

---

## 🟡 Broken

Se utiliza cuando ocurre un error técnico no controlado.

Ejemplos:

```text
Appium Server no disponible
Database connection failed
API connection error
Driver no inicializado
```

Esta separación facilita identificar rápidamente si el problema está en:

```text
🔴 Funcionalidad
```

o:

```text
🟡 Infraestructura / Automatización
```

---

# 🔄 Background y precondiciones

`Background` se utiliza para definir condiciones iniciales comunes a todos los escenarios de una Feature.

En este framework se recomienda utilizarlo principalmente para:

- Precondiciones de Base de Datos.
- Preparación de datos.
- Validaciones iniciales de API.
- Estado inicial necesario para ejecutar el escenario.

Ejemplo:

```gherkin
@database @api
Feature: Transferencias

    Background:

        Given existe el usuario "standard_user"

        And la cuenta del usuario está activa

        And el servicio de transferencias está disponible

    Scenario: Transferencia exitosa

        When realiza una transferencia de 100 USD

        Then la transferencia debería realizarse correctamente
```

La idea es:

```text
Background
    ↓
Preparar condiciones iniciales
    ↓
Scenario
    ↓
Ejecutar acción
    ↓
Then
    ↓
Validar resultado
```

No se recomienda utilizar el `Background` para colocar las validaciones principales del escenario.

---

# 🏷️ Tags

Los Tags permiten activar los recursos necesarios para cada escenario.

## API

```gherkin
@api
Scenario: Consultar Pokemon
```

## Database

```gherkin
@database
Scenario: Validar usuarios
```

## Combinación

```gherkin
@api @database
Scenario: Validación integrada
```

El `environment.py` utiliza estos Tags para inicializar los recursos correspondientes.

---

# 🔗 Escenario integrado

El framework permite combinar Front, API y Database dentro del mismo escenario.

Ejemplo:

```gherkin
@api @database
Scenario: Validación integrada

    Given que el usuario abre la aplicación

    When ingresa el usuario "standard_user"
    And ingresa la contraseña "secret_sauce"
    And presiona el botón LOGIN

    Then debería ingresar correctamente a la aplicación

    When consulto el Pokemon "pikachu"

    Then la API debería responder con código 200
    And el Pokemon debería llamarse "pikachu"

    And debería existir información de usuarios en la base de datos
```

El reporte puede mostrar:

```text
✓ Login
    📎 Screenshot

✓ Validación de Login
    📎 Screenshot
    📎 Assertion
    📎 Expected
    📎 Actual

✓ Consulta API
    📎 Method
    📎 Endpoint
    📎 Status Code
    📎 Response

✓ Validación API
    📎 Assertion
    📎 Expected
    📎 Actual

✓ Consulta BD
    📎 SQL Query
    📎 Parameters
    📎 Result
```

Esto permite tener trazabilidad completa del escenario.

---

# ⚙️ Configuración

El framework utiliza variables de entorno para información sensible y configuración.

Ejemplo:

```env
APPIUM_SERVER=http://127.0.0.1:4723

PLATFORM_NAME=Android
DEVICE_NAME=emulator-5554

APP_PACKAGE=com.example.app
APP_ACTIVITY=.MainActivity

DB_HOST=localhost
DB_PORT=1521
DB_SERVICE=XEPDB1
DB_USER=usuario
DB_PASSWORD=password
```

---

# 🔐 Seguridad

Nunca almacenar en el código:

- Passwords.
- Tokens.
- Credenciales.
- Información sensible.
- Variables de conexión.

Utilizar `.env`.

Agregar al `.gitignore`:

```gitignore
.env
venv/
.venv/
__pycache__/
allure-results/
allure-report/
screenshots/
```

---

# 💻 Requisitos

Antes de instalar el framework se necesita:

- Python 3.x
- Node.js
- npm
- Java JDK
- Android Studio
- Android SDK
- Android SDK Platform Tools
- Android Emulator o dispositivo físico
- Appium 2
- UiAutomator2
- Allure Commandline
- Git
- Oracle Database o acceso a una instancia Oracle

---

# 🚀 Instalación

## 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd proyecto__python
```

---

## 2. Crear entorno virtual

```bash
python -m venv venv
```

### Git Bash

```bash
source venv/Scripts/activate
```

### PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

### CMD

```cmd
venv\Scripts\activate
```

Verificar:

```bash
python --version
```

---

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

Dependencias principales:

```text
Appium-Python-Client
behave
selenium
requests
oracledb
python-dotenv
allure-behave
```

Si se agregan nuevas dependencias:

```bash
pip freeze > requirements.txt
```

---

# 📱 Configuración Android

## Verificar ADB

```bash
adb --version
```

Ver dispositivos:

```bash
adb devices
```

Ejemplo:

```text
List of devices attached
emulator-5554    device
```

---

## Ver emuladores

```bash
emulator -list-avds
```

Iniciar:

```bash
emulator -avd Pixel_7
```

Después:

```bash
adb devices
```

---

# 📲 Instalar Appium

Verificar Node:

```bash
node --version
npm --version
```

Instalar Appium:

```bash
npm install -g appium
```

Verificar:

```bash
appium --version
```

---

# 🤖 Instalar UiAutomator2

```bash
appium driver install uiautomator2
```

Verificar:

```bash
appium driver list
```

---

# ▶️ Iniciar Appium

Abrir una terminal:

```bash
appium
```

Por defecto:

```text
http://127.0.0.1:4723
```

Mantener el servidor activo durante la ejecución.

---

# 📦 Instalar APK

Si se dispone de un APK:

```bash
adb install "app/application.apk"
```

Resultado esperado:

```text
Success
```

---

# 🔍 Obtener Package y Activity

Con la aplicación abierta:

### Windows CMD

```cmd
adb shell dumpsys window | findstr mCurrentFocus
```

Ejemplo:

```text
mCurrentFocus=Window{... u0 com.example.app/com.example.app.MainActivity}
```

Configurar:

```env
APP_PACKAGE=com.example.app
APP_ACTIVITY=.MainActivity
```

---

# 🔎 Appium Inspector

Appium Inspector permite identificar los elementos de la aplicación y obtener locators.

Flujo:

```text
Appium
   ↓
Appium Inspector
   ↓
Android Device / Emulator
   ↓
Aplicación
```

Se recomienda utilizar:

```text
Accessibility ID
```

antes que XPath cuando exista un identificador estable.

---

# 🗄️ Configuración Database

Crear un archivo:

```text
.env
```

Ejemplo:

```env
DB_HOST=localhost
DB_PORT=1521
DB_SERVICE=XEPDB1
DB_USER=usuario
DB_PASSWORD=password
```

La conexión se realiza mediante:

```python
DatabaseConnection()
```

Los repositories utilizan las queries centralizadas en:

```text
database/queries.py
```

---

# 🧪 Ejecución de pruebas

## Todos los escenarios

```bash
behave
```

---

## Feature específico

```bash
behave features/login.feature
```

---

## Escenario específico

```bash
behave --name "Login exitoso con credenciales válidas"
```

---

## Por Tag

```bash
behave --tags=smoke
```

API:

```bash
behave -t @api
```

Database:

```bash
behave -t @database
```

---

# 📊 Ejecución con Allure

Generar resultados:

```bash
behave -f allure_behave.formatter:AllureFormatter -o allure-results
```

Generar reporte:

```bash
allure generate allure-results -o allure-report --clean
```

Abrir:

```bash
allure open allure-report
```

También puede utilizarse:

```bash
allure serve allure-results
```

---

# 🧹 Limpiar resultados

### Git Bash

```bash
rm -rf allure-results
rm -rf allure-report
```

### CMD

```cmd
rmdir /s /q allure-results
rmdir /s /q allure-report
```

---

# 🧹 Script de ejecución

Si el proyecto utiliza:

```text
run_tests.sh
```

el script puede automatizar:

```text
Limpiar resultados
       ↓
Limpiar reporte
       ↓
Ejecutar Behave
       ↓
Generar Allure
       ↓
Abrir / generar reporte
```

Ejecutar:

```bash
./run_tests.sh
```

---

# 🛡️ Buenas prácticas

## Esperas explícitas

Evitar:

```python
time.sleep(5)
```

Preferir:

```python
WebDriverWait(driver, 15)
```

---

## Locators estables

Preferir:

```python
AppiumBy.ACCESSIBILITY_ID
```

sobre XPath cuando exista un identificador estable.

---

## Separación de responsabilidades

### Step

```python
context.login_page.enter_username(username)
```

### Page Object

```python
def enter_username(self, username):
    self.enter_text(
        self.USERNAME,
        username
    )
```

### Base Page

```python
def enter_text(self, locator, text):
    element = self.find_element(locator)
    element.clear()
    element.send_keys(text)
```

Cada capa tiene una responsabilidad diferente.

---

# 🔧 Troubleshooting

## Appium no encuentra el dispositivo

Ejecutar:

```bash
adb devices
```

Verificar:

- USB Debugging.
- Autorización del dispositivo.
- Android SDK.
- `ANDROID_HOME`.
- `adb`.

---

## Appium no encuentra un elemento

Verificar el locator en Appium Inspector.

También comprobar:

- Que la aplicación esté en la pantalla correcta.
- Que el elemento esté visible.
- Que el locator siga siendo válido.
- Que se esté utilizando una espera explícita.

---

## Allure muestra Broken en lugar de Failed

`Broken` normalmente representa un error técnico no controlado.

Ejemplo:

```text
TimeoutException
ConnectionError
Database connection error
```

Si el problema representa una **validación funcional**, debe utilizarse `verify()` para convertirlo en una validación con Expected / Actual.

Ejemplo:

```text
Expected:
PRODUCTS

Actual:
PRODUCTS no encontrado
```

Esto permite que Allure lo clasifique como:

```text
Failed
```

---

## No aparece evidencia de Database

Verificar:

1. El escenario tiene `@database`.
2. Existe conexión a Oracle.
3. El Repository utiliza `execute_query()`.
4. La consulta realmente fue ejecutada.
5. Se generaron nuevos `allure-results`.

---

## No aparece evidencia de API

Verificar:

1. El escenario tiene `@api`.
2. `ApiClient` está inicializado.
3. La llamada pasa por `ApiClient`.
4. Se generaron nuevos `allure-results`.

---

# 📈 Roadmap

## Implementado

- [x] Python
- [x] Appium
- [x] UiAutomator2
- [x] Behave
- [x] Gherkin
- [x] Page Object Model
- [x] Esperas explícitas
- [x] Oracle Database
- [x] Repository Pattern
- [x] Queries centralizadas
- [x] API Client
- [x] Integración REST
- [x] Assertions reutilizables
- [x] Screenshots por Step
- [x] Evidencia SQL
- [x] Evidencia API
- [x] Expected / Actual
- [x] Allure
- [x] Background para precondiciones
- [x] Escenarios Front + API + Database

## Próximas mejoras

- [ ] Test Data Factory
- [ ] Datos dinámicos de prueba
- [ ] Configuración por ambientes
- [ ] Fixtures reutilizables
- [ ] Ejecución paralela
- [ ] Ejecución multi-device
- [ ] Videos de ejecución
- [ ] Integración GitHub Actions
- [ ] Integración Jenkins
- [ ] Ejecución en dispositivos Cloud
- [ ] Histórico de resultados
- [ ] Dockerización del framework

---

# 📋 Comandos rápidos

| Acción | Comando |
|---|---|
| Activar venv | `source venv/Scripts/activate` |
| Ver Python | `python --version` |
| Ver ADB | `adb --version` |
| Ver dispositivos | `adb devices` |
| Ver emuladores | `emulator -list-avds` |
| Iniciar emulador | `emulator -avd Pixel_7` |
| Ver Appium | `appium --version` |
| Iniciar Appium | `appium` |
| Instalar UiAutomator2 | `appium driver install uiautomator2` |
| Instalar APK | `adb install "app/application.apk"` |
| Ejecutar todos | `behave` |
| Ejecutar Login | `behave features/login.feature` |
| Ejecutar Smoke | `behave --tags=smoke` |
| Ejecutar API | `behave -t @api` |
| Ejecutar Database | `behave -t @database` |
| Generar Allure | `behave -f allure_behave.formatter:AllureFormatter -o allure-results` |
| Generar reporte | `allure generate allure-results -o allure-report --clean` |
| Abrir Allure | `allure open allure-report` |
| Servir Allure | `allure serve allure-results` |
| Ejecutar framework | `./run_tests.sh` |

---

# 👨‍💻 Autor

Proyecto de automatización Mobile desarrollado con **Python, Appium y Behave**, extendido con integración de **APIs REST, Oracle Database, Assertions reutilizables y Allure** para generar evidencia detallada por Step.

---

## 📚 Referencias

- Appium: https://appium.io/
- Behave: https://behave.readthedocs.io/
- Allure: https://allurereport.org/
- Python: https://www.python.org/
- Android Developers: https://developer.android.com/
