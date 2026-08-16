import os
import json
import shutil
import hashlib
import subprocess

from config.devices import ANDROID_DEVICES


# =============================================================
# CONFIGURACIÓN
# =============================================================

ALLURE_RESULTS = "allure-results"


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
    print(f"Device: {device_name}")
    print(f"Platform: {platform}")
    print(f"Version: {platform_version}")
    print(f"Execution: {execution}")
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
    # RECORRER ARCHIVOS DE RESULTADOS
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

            # =================================================
            # ELIMINAR PARÁMETROS ANTERIORES
            # =================================================

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

            # =================================================
            # DEVICE
            # =================================================

            parameters.append({
                "name": "Device",
                "value": device_name
            })

            # =================================================
            # PLATFORM
            # =================================================

            parameters.append({
                "name": "Platform",
                "value": platform
            })

            # =================================================
            # VERSION
            # =================================================

            parameters.append({
                "name": "Version",
                "value": platform_version
            })

            # =================================================
            # EXECUTION
            # =================================================

            parameters.append({
                "name": "Execution",
                "value": execution
            })

            result["parameters"] = parameters
            # =========================================================
            # ALLURE SUITES
            # =========================================================

            labels = result.get(
                "labels",
                []
            )

            # ---------------------------------------------------------
            # ELIMINAR SUITES ANTERIORES
            # ---------------------------------------------------------

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

            # ---------------------------------------------------------
            # PARENT SUITE
            # ---------------------------------------------------------

            labels.append({
                "name": "parentSuite",
                "value": "LambdaTest"
            })

            # ---------------------------------------------------------
            # SUITE = DISPOSITIVO
            # ---------------------------------------------------------

            labels.append({
                "name": "suite",
                "value": device_name
            })

            # ---------------------------------------------------------
            # SUB SUITE = FEATURE
            # ---------------------------------------------------------

            feature_name = result.get(
                "name",
                "Unknown"
            )

            labels.append({
                "name": "subSuite",
                "value": feature_name
            })

            result["labels"] = labels

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
            # CREAR IDENTIFICADOR ÚNICO POR DISPOSITIVO
            # =================================================

            history_key = (
                f"{original_history_id}|"
                f"Device={device_name}|"
                f"Platform={platform}|"
                f"Version={platform_version}"
            )

            new_history_id = hashlib.md5(
                history_key.encode(
                    "utf-8"
                )
            ).hexdigest()

            result["historyId"] = (
                new_history_id
            )

            # =================================================
            # GUARDAR JSON
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

    # =========================================================
    # LIMPIAR RESULTADOS ANTERIORES
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
    print("🧹 ALLURE RESULTS LIMPIADO")
    print("=" * 60)

    # =========================================================
    # RECORRER DISPOSITIVOS
    # =========================================================

    for index, device in enumerate(
        ANDROID_DEVICES
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
        # LIMPIAR RESULTADOS TEMPORALES
        # =====================================================

        if os.path.exists(
            device_results
        ):

            shutil.rmtree(
                device_results
            )

        # =====================================================
        # INFORMACIÓN DEL DISPOSITIVO
        # =====================================================

        print("\n")
        print("=" * 60)
        print("📱 EJECUTANDO TEST EN LAMBDATEST")
        print("=" * 60)

        print(
            f"Device: {device_name}"
        )

        print(
            f"Android: {platform_version}"
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

        environment[
            "LT_DEVICE_INDEX"
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
        # ACTUALIZAR INFORMACIÓN ALLURE
        # =====================================================

        add_device_to_allure_results(

            results_directory=device_results,

            device_name=device_name,

            platform="Android",

            platform_version=platform_version,

            execution="LambdaTest"
        )

        # =====================================================
        # COPIAR RESULTADOS AL DIRECTORIO FINAL
        # =====================================================

        merge_allure_results(
            device_results
        )

        # =====================================================
        # ELIMINAR DIRECTORIO TEMPORAL
        # =====================================================

        if os.path.exists(
            device_results
        ):

            shutil.rmtree(
                device_results
            )

        # =====================================================
        # RESULTADO DE LA EJECUCIÓN
        # =====================================================

        if result.returncode == 0:

            print("\n")
            print(
                "✅ TEST FINALIZADO"
            )

            print(
                f"📱 Dispositivo: "
                f"{device_name}"
            )

        else:

            print("\n")
            print(
                "❌ TEST FALLÓ"
            )

            print(
                f"📱 Dispositivo: "
                f"{device_name}"
            )


# =============================================================
# MAIN
# =============================================================

if __name__ == "__main__":

    run_tests_on_devices()