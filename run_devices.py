import os
import json
import shutil
import hashlib
import subprocess


from config.config import (
    EXECUTION_PLATFORM,
    PLATFORM_NAME
)

from config.devices import (
    LAMBDATEST_ANDROID_DEVICES,
    LAMBDATEST_IOS_DEVICES,
    BROWSERSTACK_ANDROID_DEVICES,
    BROWSERSTACK_IOS_DEVICES
)


# =============================================================
# CONFIGURACIÓN
# =============================================================

ALLURE_RESULTS = "allure-results"


# =============================================================
# OBTENER DISPOSITIVOS
# =============================================================

def get_devices():

    execution = EXECUTION_PLATFORM.lower()

    platform = PLATFORM_NAME.lower()

    # =========================================================
    # LAMBDATEST
    # =========================================================

    if execution == "lambdatest":

        if platform == "android":

            return LAMBDATEST_ANDROID_DEVICES

        elif platform == "ios":

            return LAMBDATEST_IOS_DEVICES

    # =========================================================
    # BROWSERSTACK
    # =========================================================

    elif execution == "browserstack":

        if platform == "android":

            return BROWSERSTACK_ANDROID_DEVICES

        elif platform == "ios":

            return BROWSERSTACK_IOS_DEVICES

    raise ValueError(
        f"No existen dispositivos configurados "
        f"para {execution} / {platform}"
    )


# =============================================================
# OBTENER NOMBRE DEL ÍNDICE
# =============================================================

def get_device_index_variable():

    execution = EXECUTION_PLATFORM.lower()

    if execution == "lambdatest":

        return "LT_DEVICE_INDEX"

    elif execution == "browserstack":

        return "BS_DEVICE_INDEX"

    else:

        raise ValueError(
            f"Multi-device no soportado para: "
            f"{execution}"
        )


# =============================================================
# ACTUALIZAR RESULTADOS DE ALLURE
# =============================================================

def add_device_to_allure_results(
    results_directory,
    device_name,
    platform,
    platform_version,
    execution
):

    print("\n")
    print("=================================")
    print("📊 ACTUALIZANDO ALLURE")
    print("=================================")

    print(
        f"Provider: {execution}"
    )

    print(
        f"Device: {device_name}"
    )

    print(
        f"Platform: {platform}"
    )

    print(
        f"Version: {platform_version}"
    )

    print("=================================")

    if not os.path.exists(
        results_directory
    ):

        print(
            "⚠️ No existe el directorio:"
        )

        print(
            results_directory
        )

        return

    # =========================================================
    # RECORRER RESULTADOS
    # =========================================================

    for filename in os.listdir(
        results_directory
    ):

        if not filename.endswith(
            "-result.json"
        ):

            continue

        filepath = os.path.join(
            results_directory,
            filename
        )

        try:

            # =================================================
            # LEER JSON
            # =================================================

            with open(
                filepath,
                "r",
                encoding="utf-8"
            ) as file:

                result = json.load(file)

            # =================================================
            # PARAMETERS
            # =================================================

            parameters = result.get(
                "parameters",
                []
            )

            # -------------------------------------------------
            # ELIMINAR PARÁMETROS ANTERIORES
            # -------------------------------------------------

            parameters = [
                parameter
                for parameter in parameters
                if parameter.get("name")
                not in [
                    "Device",
                    "Platform",
                    "Version",
                    "Execution"
                ]
            ]

            # -------------------------------------------------
            # DEVICE
            # -------------------------------------------------

            parameters.append({
                "name":
                    "Device",

                "value":
                    device_name
            })

            # -------------------------------------------------
            # PLATFORM
            # -------------------------------------------------

            parameters.append({
                "name":
                    "Platform",

                "value":
                    platform
            })

            # -------------------------------------------------
            # VERSION
            # -------------------------------------------------

            parameters.append({
                "name":
                    "Version",

                "value":
                    platform_version
            })

            # -------------------------------------------------
            # EXECUTION
            # -------------------------------------------------

            parameters.append({
                "name":
                    "Execution",

                "value":
                    execution
            })

            result[
                "parameters"
            ] = parameters

            # =================================================
            # ALLURE SUITES
            # =================================================

            labels = result.get(
                "labels",
                []
            )

            # -------------------------------------------------
            # ELIMINAR SUITES ANTERIORES
            # -------------------------------------------------

            labels = [
                label
                for label in labels
                if label.get("name")
                not in [
                    "parentSuite",
                    "suite",
                    "subSuite"
                ]
            ]

            # -------------------------------------------------
            # PARENT SUITE
            # -------------------------------------------------

            labels.append({
                "name":
                    "parentSuite",

                "value":
                    execution
            })

            # -------------------------------------------------
            # SUITE = DISPOSITIVO
            # -------------------------------------------------

            labels.append({
                "name":
                    "suite",

                "value":
                    device_name
            })

            # -------------------------------------------------
            # SUB SUITE = FEATURE
            # -------------------------------------------------

            feature_name = result.get(
                "name",
                "Unknown"
            )

            labels.append({
                "name":
                    "subSuite",

                "value":
                    feature_name
            })

            result[
                "labels"
            ] = labels

            # =================================================
            # HISTORY ID
            # =================================================

            original_history_id = result.get(
                "historyId"
            )

            if not original_history_id:

                original_history_id = result.get(
                    "testCaseId"
                )

            if not original_history_id:

                original_history_id = result.get(
                    "fullName"
                )

            if not original_history_id:

                original_history_id = result.get(
                    "uuid"
                )

            # =================================================
            # IDENTIFICADOR POR PROVEEDOR + DISPOSITIVO
            # =================================================

            history_key = (
                f"{original_history_id}|"
                f"Execution={execution}|"
                f"Device={device_name}|"
                f"Platform={platform}|"
                f"Version={platform_version}"
            )

            new_history_id = hashlib.md5(
                history_key.encode(
                    "utf-8"
                )
            ).hexdigest()

            result[
                "historyId"
            ] = new_history_id

            # =================================================
            # GUARDAR
            # =================================================

            with open(
                filepath,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    result,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            print(
                f"✅ Actualizado: {filename}"
            )

            print(
                f"   Provider: {execution}"
            )

            print(
                f"   Device: {device_name}"
            )

            print(
                f"   Version: {platform_version}"
            )

            print(
                f"   History ID: {new_history_id}"
            )

        except Exception as e:

            print(
                f"❌ Error procesando "
                f"{filename}"
            )

            print(e)


# =============================================================
# MERGE DE RESULTADOS
# =============================================================

def merge_allure_results(
    source_directory
):

    if not os.path.exists(
        source_directory
    ):

        return

    os.makedirs(
        ALLURE_RESULTS,
        exist_ok=True
    )

    # =========================================================
    # COPIAR ARCHIVOS
    # =========================================================

    for filename in os.listdir(
        source_directory
    ):

        source = os.path.join(
            source_directory,
            filename
        )

        destination = os.path.join(
            ALLURE_RESULTS,
            filename
        )

        if os.path.isfile(
            source
        ):

            shutil.copy2(
                source,
                destination
            )

            print(
                f"📦 Copiado: {filename}"
            )


# =============================================================
# EJECUTAR TESTS EN DISPOSITIVOS
# =============================================================

def run_tests_on_devices():

    execution = (
        EXECUTION_PLATFORM.lower()
    )

    platform = (
        PLATFORM_NAME
    )

    # =========================================================
    # VALIDAR PLATAFORMA
    # =========================================================

    if execution not in [
        "lambdatest",
        "browserstack"
    ]:

        raise ValueError(
            "run_devices.py solamente soporta "
            "LambdaTest y BrowserStack."
        )

    # =========================================================
    # OBTENER DISPOSITIVOS
    # =========================================================

    devices = get_devices()

    # =========================================================
    # OBTENER VARIABLE DE ÍNDICE
    # =========================================================

    device_index_variable = (
        get_device_index_variable()
    )

    # =========================================================
    # LIMPIAR RESULTADOS
    # =========================================================

    if os.path.exists(
        ALLURE_RESULTS
    ):

        shutil.rmtree(
            ALLURE_RESULTS
        )

    os.makedirs(
        ALLURE_RESULTS
    )

    print("\n")
    print("=" * 60)
    print("🚀 MULTI-DEVICE EXECUTION")
    print("=" * 60)

    print(
        f"Provider: {execution}"
    )

    print(
        f"Platform: {platform}"
    )

    print(
        f"Devices: {len(devices)}"
    )

    print("=" * 60)

    # =========================================================
    # VARIABLES DE CONTROL
    # =========================================================

    total_devices = len(
        devices
    )

    successful_devices = 0

    failed_devices = 0

    # =========================================================
    # RECORRER DISPOSITIVOS
    # =========================================================

    for index, device in enumerate(
        devices
    ):

        device_name = device[
            "name"
        ]

        platform_version = device[
            "platform_version"
        ]

        # =====================================================
        # DIRECTORIO TEMPORAL
        # =====================================================

        device_results = (
            f"allure-results-device-{index}"
        )

        # =====================================================
        # LIMPIAR RESULTADO TEMPORAL
        # =====================================================

        if os.path.exists(
            device_results
        ):

            shutil.rmtree(
                device_results
            )

        # =====================================================
        # INFORMACIÓN
        # =====================================================

        print("\n")
        print("=" * 60)

        print(
            f"📱 EJECUTANDO "
            f"{execution.upper()}"
        )

        print("=" * 60)

        print(
            f"Device: {device_name}"
        )

        print(
            f"{platform}: {platform_version}"
        )

        print(
            f"Index: {index}"
        )

        print(
            f"Results: {device_results}"
        )

        print("=" * 60)

        # =====================================================
        # VARIABLES DE ENTORNO
        # =====================================================

        environment = os.environ.copy()

        # -----------------------------------------------------
        # PROVIDER
        # -----------------------------------------------------

        environment[
            "EXECUTION_PLATFORM"
        ] = execution

        # -----------------------------------------------------
        # DEVICE INDEX
        # -----------------------------------------------------

        environment[
            device_index_variable
        ] = str(index)

        # =====================================================
        # EJECUTAR BEHAVE
        # =====================================================

        result = subprocess.run(

            [
                "behave",

                "-t",
                "@smoke",

                "-f",
                "allure_behave.formatter:AllureFormatter",

                "-o",
                device_results
            ],

            env=environment
        )

        # =====================================================
        # ACTUALIZAR ALLURE
        # =====================================================

        add_device_to_allure_results(

            results_directory=device_results,

            device_name=device_name,

            platform=platform,

            platform_version=platform_version,

            execution=execution
        )

        # =====================================================
        # MERGE
        # =====================================================

        merge_allure_results(
            device_results
        )

        # =====================================================
        # ELIMINAR TEMPORAL
        # =====================================================

        if os.path.exists(
            device_results
        ):

            shutil.rmtree(
                device_results
            )

        # =====================================================
        # RESULTADO
        # =====================================================

        if result.returncode == 0:

            successful_devices += 1

            print("\n")
            print(
                "✅ TEST FINALIZADO"
            )

            print(
                f"📱 Dispositivo: "
                f"{device_name}"
            )

        else:

            failed_devices += 1

            print("\n")
            print(
                "❌ TEST FALLÓ"
            )

            print(
                f"📱 Dispositivo: "
                f"{device_name}"
            )

    # =========================================================
    # RESUMEN
    # =========================================================

    print("\n")
    print("=" * 60)
    print("📊 RESUMEN DE EJECUCIÓN")
    print("=" * 60)

    print(
        f"Provider: {execution}"
    )

    print(
        f"Platform: {platform}"
    )

    print(
        f"Total dispositivos: {total_devices}"
    )

    print(
        f"✅ Exitosos: {successful_devices}"
    )

    print(
        f"❌ Fallidos: {failed_devices}"
    )

    print("=" * 60)

    # =========================================================
    # RETURN CODE
    # =========================================================

    if failed_devices > 0:

        return 1

    return 0


# =============================================================
# MAIN
# =============================================================

if __name__ == "__main__":

    exit_code = (
        run_tests_on_devices()
    )

    raise SystemExit(
        exit_code
    )