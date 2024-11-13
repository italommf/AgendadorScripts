@echo off
REM Ative o ambiente virtual
call ..\.venv\Scripts\activate.bat

REM Navegue até o diretório onde o manage.py está localizado
cd /d "%~dp0"

REM Execute o servidor Django em segundo plano
start /b python manage.py runserver

REM O script termina aqui, pois você não quer que a janela fique aberta
