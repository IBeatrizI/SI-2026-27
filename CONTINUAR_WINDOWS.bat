@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
  echo ERRO: Python launcher nao encontrado. Verifica com py --version.
  pause
  exit /b 1
)
echo === FASE 2: testar, validar os originais e gerar analises REAIS ===
echo [1/6] Testes locais...
py -m unittest discover -s tests -v
if errorlevel 1 goto erro
echo [2/6] Reprocessar originais existentes (SEM descarregar outra vez)...
py scripts\preparar_dw.py
if errorlevel 1 goto erro
echo [3/6] Validar chaves, totais e granularidade...
py scripts\validar_dw.py
if errorlevel 1 goto erro
echo [4/6] Reconciliar independentemente com CSVs originais...
py scripts\validar_origem_e_dw.py
if errorlevel 1 goto erro
echo [5/6] Gerar tabelas analiticas...
py scripts\gerar_analises.py
if errorlevel 1 goto erro
echo [6/6] Resultado: consultar data\analysis\ e docs\09_resultados_exploratorios_reais.md
echo SUCESSO: Fase 2 verificada e tabelas de apoio prontas para Power BI.
pause
exit /b 0
:erro
echo FALHA. Nao considerar concluidos os passos seguintes.
pause
exit /b 1
