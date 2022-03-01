@echo off
:start
echo Please input the dir to be remove:
set /p input=
echo Please confirm the dir you want to remove: %input% [y/n] (y for yes, n for no)
set /p confirm=
if "%confirm%"=="n" goto exit
if "%confirm%"=="y" goto begin
goto start
:begin
set save_file=saved_resource(2)
set suffix=html
if "%input%"=="" goto exit
for /f %%i in ('dir /b /a-d /s "%input%"') do (
        echo %%i | findstr %save_file% > nul && echo save %%i || del %%i
)

:exit
pause