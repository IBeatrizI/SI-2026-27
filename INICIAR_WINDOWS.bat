@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
  echo ERRO: Python Launcher nao encontrado. Verificar com py --version.
  pause
  exit /b 1
)
echo === FASE 2: recolha E-REDES, ETL, validacoes e analise ===
echo [1/7] Testes locais sinteticos...
py -m unittest discover -s tests -v
if errorlevel 1 goto erro
echo [2/7] Descarregar E-REDES 2021-2024 (Internet)...
py scripts\descarregar_e_redes.py --anos 2021 2022 2023 2024
if errorlevel 1 goto erro
echo [3/7] Perfil dos CSV originais...
py scripts\perfil_e_redes.py
if errorlevel 1 goto erro
echo [4/7] Preparar dimensoes e facto...
py scripts\preparar_dw.py
if errorlevel 1 goto erro
echo [5/7] Validar modelo dimensional...
py scripts\validar_dw.py
if errorlevel 1 goto erro
echo [6/7] Reconciliacao independente por mes x distrito x tensao...
py scripts\validar_origem_e_dw.py
if errorlevel 1 goto erro
echo [7/7] Gerar analises exploratorias reais...
py scripts\gerar_analises.py
if errorlevel 1 goto erro
echo SUCESSO: rever data\quality, data\analysis e docs\09_resultados_exploratorios_reais.md
pause
exit /b 0
:erro
echo FALHA: corrigir antes de utilizar resultados. Consultar docs\GUIA_EXECUCAO.md
pause
exit /b 1
