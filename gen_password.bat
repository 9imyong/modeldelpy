@echo off
REM Usage: gen_password.bat <plain_password>
IF "%~1"=="" (
  ECHO Usage: %~nx0 ^<plain_password^>
  EXIT /b 1
)
SETLOCAL ENABLEDELAYEDEXPANSION
SET PLAIN_PASS=%~1
REM Python 스크립트 호출로 해시 생성
FOR /F "usebackq delims=" %%H IN (`python -c "from utils.security import hash_password; print(hash_password(r'!PLAIN_PASS!'))"`) DO (
    SET HASH=%%H
)
SET ENV_FILE=%~dp0\.env
REM .env 업데이트
powershell -NoProfile -Command "(Get-Content '%ENV_FILE%') -replace '^(ADMIN_PASSWORD_HASH)=.*', 'ADMIN_PASSWORD_HASH=!HASH!' | Set-Content '%ENV_FILE%'"
ECHO Updated ADMIN_PASSWORD_HASH in .env: !HASH!
ENDLOCAL