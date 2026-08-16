# 📱 Mobile Automation Framework - Python

Framework de automatización de pruebas para aplicaciones móviles desarrollado con **Python, Appium y Behave**, integrado con **LambdaTest**, **Allure Reports**, **Oracle Database** y automatización de APIs REST.

El framework está diseñado para soportar pruebas de:

- 📱 Aplicaciones móviles Android e iOS
- 🌐 APIs REST
- 🗄️ Base de datos Oracle
- 🔗 Pruebas de integración Front + API + Base de Datos
- ☁️ Ejecución en dispositivos reales mediante LambdaTest
- 📊 Reportes detallados con Allure
- 📱 Ejecución sobre múltiples dispositivos

---

# 🛠️ Tecnologías

| Tecnología | Uso |
|---|---|
| Python | Lenguaje principal |
| Behave | BDD / Gherkin |
| Appium | Automatización Mobile |
| UiAutomator2 | Automatización Android |
| XCUITest | Automatización iOS |
| LambdaTest | Dispositivos móviles reales |
| Requests | Automatización API |
| OracleDB | Conexión a Base de Datos |
| Allure | Reportes |
| python-dotenv | Manejo de configuración |
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
├── screenshots/
│
├── allure-results/
│
├── .env
├── .gitignore
├── README.md
├── requirements.txt
├── run_devices.py
├── run_tests.sh
└── test_appium.py