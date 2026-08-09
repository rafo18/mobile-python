#!/bin/bash

echo "========================================"
echo " Limpiando reportes anteriores..."
echo "========================================"

rm -rf allure-results
rm -rf allure-report

mkdir -p allure-results

echo ""
echo "========================================"
echo " Ejecutando pruebas..."
echo "========================================"

behave -f allure_behave.formatter:AllureFormatter -o allure-results

TEST_RESULT=$?

echo ""
echo "========================================"
echo " Generando reporte Allure..."
echo "========================================"

allure generate allure-results -o allure-report --clean

echo ""
echo "========================================"
echo " Reporte generado correctamente"
echo "========================================"

if [ $TEST_RESULT -ne 0 ]; then
    echo "⚠️ Algunas pruebas fallaron."
else
    echo "✅ Todas las pruebas pasaron."
fi

exit $TEST_RESULT