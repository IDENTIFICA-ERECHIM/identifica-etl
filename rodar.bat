@echo off
setlocal

cd /d "%~dp0"

docker compose up -d mysql
if errorlevel 1 goto erro

docker compose run --rm --build etl
if errorlevel 1 goto erro

echo.
echo ETL concluido. Estado do banco:
docker compose ps
if errorlevel 1 goto erro

echo.
echo Execucao finalizada com sucesso!
pause
exit /b 0

:erro
echo.
echo ERRO: ocorreu uma falha durante a execucao.
pause
exit /b 1
