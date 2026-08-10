# 📱 Mobile Automation Framework

Framework de automatización de pruebas móviles desarrollado con **Python, Appium, Behave y Gherkin**, utilizando el patrón de diseño **Page Object Model (POM)** y **Allure** para la generación de reportes.

El proyecto está orientado a la automatización de aplicaciones Android mediante un **Android Emulator** o dispositivo físico.

---

## 🛠️ Tecnologías

- **Python** - Lenguaje de programación
- **Appium** - Automatización mobile
- **UiAutomator2** - Automatización Android
- **Behave** - Framework BDD
- **Gherkin** - Definición de escenarios
- **Selenium** - Esperas explícitas y utilidades
- **Allure** - Reportería
- **ADB** - Comunicación con dispositivos Android
- **Android Studio** - Emulador y Android SDK
- **Git / GitHub** - Control de versiones

---

## 📂 Estructura del proyecto

```text
proyecto__python/
│
├── app/
│   └── application.apk
│
├── features/
│   ├── login.feature
│   ├── environment.py
│   │
│   └── steps/
│       └── login_steps.py
│
├── pages/
│   ├── base_page.py
│   └── login_page.py
│
├── drivers/
│   └── driver_factory.py
│
├── config/
│   └── config.py
│
├── database/
│   ├── connection.py
│   └── queries.py
│
├── test_data/
│
├── screenshots/
│
├── allure-results/
│
├── allure-report/
│
├── venv/
│
├── .env
├── .gitignore
├── requirements.txt
├── run_tests.sh
└── README.md
```

> `venv/`, `allure-results/`, `allure-report/` y archivos sensibles como `.env` no deben subirse al repositorio.

---

# 🏗️ Arquitectura

El proyecto utiliza **Page Object Model (POM)** para separar la lógica de las pruebas de la interacción con los elementos de la aplicación.

```text
Gherkin
   ↓
Behave
   ↓
Step Definitions
   ↓
Page Object Model
   ↓
Appium
   ↓
UiAutomator2
   ↓
Android Emulator / Device
   ↓
Aplicación Mobile
```

---

# 📁 Componentes principales

## `features/`

Contiene los escenarios escritos utilizando **Gherkin**.

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

Contiene la implementación Python de los pasos definidos en los archivos `.feature`.

Ejemplo:

```python
@when('ingresa el usuario "{username}"')
def step_enter_username(context, username):
    context.login_page.enter_username(username)
```

---

## `features/environment.py`

Contiene los hooks de Behave utilizados para realizar acciones antes o después de los escenarios.

Entre sus responsabilidades se encuentran:

- Cerrar la sesión de Appium.
- Capturar screenshots cuando un escenario falla.
- Ejecutar acciones comunes después de cada escenario.

---

## `pages/`

Contiene los Page Objects de la aplicación.

Ejemplo:

```text
pages/
├── base_page.py
├── login_page.py
├── home_page.py
└── ...
```

Cada pantalla contiene sus respectivos elementos y acciones.

---

## `pages/base_page.py`

Contiene métodos reutilizables para las diferentes pantallas.

Ejemplo:

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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

El framework utiliza **esperas explícitas** para evitar problemas de sincronización durante la carga de la aplicación.

---

## `pages/login_page.py`

Contiene los elementos y acciones correspondientes a la pantalla de Login.

Ejemplo:

```python
from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage


class LoginPage(BasePage):

    USERNAME = (
        AppiumBy.ACCESSIBILITY_ID,
        "test-Username"
    )

    PASSWORD = (
        AppiumBy.ACCESSIBILITY_ID,
        "test-Password"
    )

    LOGIN_BUTTON = (
        AppiumBy.ACCESSIBILITY_ID,
        "test-LOGIN"
    )

    def enter_username(self, username):
        self.enter_text(self.USERNAME, username)

    def enter_password(self, password):
        self.enter_text(self.PASSWORD, password)

    def click_login(self):
        self.click(self.LOGIN_BUTTON)
```

Siempre que sea posible se utilizan **Accessibility IDs** en lugar de XPath, buscando mayor estabilidad y mantenibilidad.

---

# 🚗 Driver de Appium

El archivo:

```text
drivers/driver_factory.py
```

centraliza la creación de la sesión de Appium.

Ejemplo de configuración:

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

Los valores de `app_package`, `app_activity`, dispositivo y servidor deben adaptarse al ambiente donde se ejecutará la automatización.

---

# ⚙️ Configuración

La configuración puede manejarse mediante variables de entorno.

Ejemplo de `.env`:

```env
APPIUM_SERVER=http://127.0.0.1:4723

PLATFORM_NAME=Android
DEVICE_NAME=emulator-5554

APP_PACKAGE=com.example.app
APP_ACTIVITY=.MainActivity
```

### 🔐 Seguridad

No subir al repositorio:

- Contraseñas
- Tokens
- Credenciales
- Datos sensibles
- Archivos `.env`

El archivo `.env` debe incluirse en `.gitignore`.

---

# 🗄️ Base de datos

El proyecto contempla una capa independiente para integración con base de datos:

```text
database/
├── connection.py
└── queries.py
```

Esta capa permitirá posteriormente:

- Obtener datos de prueba.
- Preparar información antes de una ejecución.
- Consultar información generada por la aplicación.
- Realizar validaciones contra la base de datos.

La implementación puede adaptarse a diferentes motores como:

- MySQL
- Oracle
- PostgreSQL
- SQLite

---

# 📸 Evidencias

Cuando un escenario falla, el framework puede capturar automáticamente un screenshot.

Las evidencias se almacenan en:

```text
screenshots/
```

Ejemplo:

```text
screenshots/
└── Login_20260809_163020.png
```

Esto permite analizar el estado de la aplicación en el momento del fallo.

---

# 📊 Reportería Allure

El proyecto utiliza **Allure** para generar reportes de ejecución.

Los resultados generados por Behave se almacenan en:

```text
allure-results/
```

El reporte HTML generado se almacena en:

```text
allure-report/
```

El reporte permite visualizar:

- Features
- Scenarios
- Steps
- Passed
- Failed
- Duración
- Errores

---

# 🧹 Script de ejecución

El archivo:

```text
run_tests.sh
```

automatiza el proceso completo de ejecución.

Cada ejecución:

```text
Eliminar resultados anteriores
        ↓
Eliminar reporte anterior
        ↓
Ejecutar Behave
        ↓
Generar resultados Allure
        ↓
Generar nuevo reporte
```

Para ejecutarlo:

```bash
./run_tests.sh
```

Esto garantiza que cada ejecución comience con resultados limpios.

---

# 💻 Requisitos

Antes de ejecutar el proyecto se necesita instalar:

- Python 3.x
- Node.js
- npm
- Java JDK
- Android Studio
- Android SDK
- Android SDK Platform Tools
- Android Emulator
- Appium 2
- UiAutomator2
- Allure Commandline
- Git

---

# 🚀 Instalación

## 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
```

Entrar al proyecto:

```bash
cd proyecto__python
```

---

## 2. Crear entorno virtual

```bash
python -m venv venv
```

Activar en Git Bash:

```bash
source venv/Scripts/activate
```

En PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Una vez activado debe aparecer:

```text
(venv)
```

---

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

Las principales dependencias utilizadas son:

```text
Appium-Python-Client
behave
selenium
allure-behave
python-dotenv
```

---

# 📱 Configuración de Android

## Verificar ADB

```bash
adb --version
```

Ver dispositivos conectados:

```bash
adb devices
```

Ejemplo:

```text
List of devices attached
emulator-5554    device
```

---

## Ver emuladores disponibles

```bash
emulator -list-avds
```

Iniciar un emulador:

```bash
emulator -avd Pixel_7
```

Después comprobar:

```bash
adb devices
```

---

# 📲 Configuración de Appium

Verificar Appium:

```bash
appium --version
```

Ver drivers:

```bash
appium driver list
```

Verificar que esté instalado:

```text
uiautomator2
```

Si no está instalado:

```bash
appium driver install uiautomator2
```

---

# ▶️ Iniciar Appium

Abrir una terminal y ejecutar:

```bash
appium
```

El servidor quedará disponible normalmente en:

```text
http://127.0.0.1:4723
```

Mantener esta terminal abierta durante la ejecución de las pruebas.

---

# 📦 Instalar el APK

Si se dispone del APK:

```bash
adb install "app/application.apk"
```

El resultado esperado es:

```text
Success
```

---

# 🔍 Obtener Package y Activity

Con la aplicación abierta:

```bash
adb shell dumpsys window | findstr mCurrentFocus
```

Ejemplo:

```text
mCurrentFocus=Window{... u0 com.example.app/com.example.app.MainActivity}
```

La configuración sería:

```env
APP_PACKAGE=com.example.app
APP_ACTIVITY=com.example.app.MainActivity
```

---

# 🧪 Ejecución de pruebas

## Ejecutar todos los escenarios

Desde la raíz del proyecto:

```bash
behave
```

---

## Ejecutar un Feature específico

```bash
behave features/login.feature
```

---

## Ejecutar un escenario específico

```bash
behave --name "Login exitoso con credenciales válidas"
```

---

## Ejecutar utilizando Tags

Ejemplo:

```gherkin
@smoke
Scenario: Login exitoso con credenciales válidas
```

Ejecutar:

```bash
behave --tags=smoke
```

Se pueden utilizar diferentes categorías:

```text
@smoke
@regression
@login
@transfer
@qr
```

---

# 📊 Ejecución con Allure

Generar resultados:

```bash
behave -f allure_behave.formatter:AllureFormatter -o allure-results
```

Generar el reporte:

```bash
allure generate allure-results -o allure-report --clean
```

Abrir el reporte:

```bash
allure open allure-report
```

---

# ⭐ Ejecución recomendada

La forma recomendada de ejecutar todo el framework es:

```bash
./run_tests.sh
```

Este comando realiza automáticamente:

1. Limpieza de resultados anteriores.
2. Limpieza del reporte anterior.
3. Ejecución de Behave.
4. Generación de resultados Allure.
5. Generación del nuevo reporte.

---

# 🔄 Flujo de ejecución

```text
                Gherkin
                   │
                   ▼
                Behave
                   │
                   ▼
            Step Definitions
                   │
                   ▼
             Page Objects
                   │
                   ▼
                Appium
                   │
                   ▼
             UiAutomator2
                   │
                   ▼
          Android Emulator
                   │
                   ▼
              Aplicación
                   │
                   ▼
          Test Result / Evidence
                   │
                   ▼
                Allure
```

---

# 🧪 Ejemplo de prueba

Actualmente el framework permite automatizar un flujo de Login.

```gherkin
Feature: Login

  Scenario: Login exitoso con credenciales válidas

    Given que el usuario abre la aplicación
    When ingresa el usuario "standard_user"
    And ingresa la contraseña "secret_sauce"
    And presiona el botón LOGIN
    Then debería ingresar correctamente a la aplicación
```

El flujo automatizado es:

```text
Abrir aplicación
       ↓
Ingresar usuario
       ↓
Ingresar contraseña
       ↓
Presionar LOGIN
       ↓
Validar Login
       ↓
Generar resultado
```

---

# 🛡️ Buenas prácticas

### Utilizar esperas explícitas

Evitar depender de:

```python
time.sleep(5)
```

Preferir:

```python
WebDriverWait(driver, 15)
```

Esto permite que la prueba espere hasta que el elemento realmente esté disponible.

---

### Utilizar locators estables

Preferir:

```python
AppiumBy.ACCESSIBILITY_ID
```

antes que XPath cuando exista un Accessibility ID disponible.

Ejemplo:

```python
USERNAME = (
    AppiumBy.ACCESSIBILITY_ID,
    "test-Username"
)
```

---

### Separar responsabilidades

Los Steps deben describir **qué hace el usuario**.

Los Page Objects deben manejar **cómo interactuar con la aplicación**.

Ejemplo:

```python
context.login_page.enter_username(username)
```

en lugar de colocar directamente:

```python
driver.find_element(...)
```

dentro del Step.

---

# 📌 Próximas mejoras

El framework puede evolucionar incorporando:

- [ ] Validaciones completas de las pantallas.
- [ ] Integración con base de datos.
- [ ] Datos dinámicos de prueba.
- [ ] Screenshots adjuntos directamente en Allure.
- [ ] Logs detallados.
- [ ] Videos de ejecución.
- [ ] Ejecución paralela.
- [ ] Configuración por ambientes.
- [ ] Smoke Testing.
- [ ] Regression Testing.
- [ ] Ejecución en múltiples dispositivos.
- [ ] Integración con GitHub Actions.
- [ ] Integración con Jenkins.
- [ ] Ejecución en dispositivos cloud.
- [ ] Histórico de resultados.

---

# 📋 Comandos rápidos

| Acción | Comando |
|---|---|
| Activar venv | `source venv/Scripts/activate` |
| Ver Python | `python --version` |
| Ver ADB | `adb --version` |
| Ver dispositivos | `adb devices` |
| Ver Appium | `appium --version` |
| Iniciar Appium | `appium` |
| Ejecutar todos los tests | `behave` |
| Ejecutar Login | `behave features/login.feature` |
| Ejecutar Smoke | `behave --tags=smoke` |
| Generar resultados Allure | `behave -f allure_behave.formatter:AllureFormatter -o allure-results` |
| Generar reporte | `allure generate allure-results -o allure-report --clean` |
| Abrir reporte | `allure open allure-report` |
| Ejecutar framework completo | `./run_tests.sh` |
|iniciar emulador| `emulator -avd Pixel_7`|
|lista de emuladores | `emulator -list-avds`|
|instalar apk| `adb install "ruta\android.apk"`|
---

# 👨‍💻 Autor

Proyecto de automatización mobile desarrollado como framework de pruebas automatizadas utilizando Python, Appium y Behave.

---