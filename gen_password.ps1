# scripts/gen_password.ps1 (Windows PowerShell용)
```powershell
Param(
    [Parameter(Mandatory=$true)]
    [string]$PlainPassword
)
# PowerShell에서 Python 스크립트 직접 호출 방식
$hash = python -c "from utils.security import hash_password; print(hash_password('$PlainPassword'))"
$envPath = "$PSScriptRoot\..\.env"
(Get-Content $envPath) -replace '^(ADMIN_PASSWORD_HASH)=.*', "`$1=$hash" | Set-Content $envPath
Write-Host "Updated ADMIN_PASSWORD_HASH in .env: $hash"