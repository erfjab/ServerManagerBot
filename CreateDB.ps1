<#
.SYNOPSIS
    Creates a new PostgreSQL database and user
.DESCRIPTION
    This script creates a new database and user in PostgreSQL with the specified credentials
#>

param (
    [string]$PgHost = "localhost",
    [int]$PgPort = 9999,
    [Parameter(Mandatory=$true)][string]$RootUser,
    [Parameter(Mandatory=$true)][string]$RootPassword,
    [Parameter(Mandatory=$true)][string]$NewDbName,
    [Parameter(Mandatory=$true)][string]$NewDbUser,
    [Parameter(Mandatory=$true)][string]$NewDbPassword
)

$psqlExe = "C:\Program Files\PostgreSQL\17\bin\psql.exe"

if (-not (Test-Path $psqlExe)) {
    Write-Host "Error: psql not found at $psqlExe" -ForegroundColor Red
    Write-Host "Please verify your PostgreSQL installation path" -ForegroundColor Yellow
    exit 1
}

$env:PGPASSWORD = $RootPassword

try {
    Write-Host ("Testing PostgreSQL connection to {0}:{1}..." -f $PgHost, $PgPort) -ForegroundColor Cyan
    $testResult = & $psqlExe -U $RootUser -h $PgHost -p $PgPort -c "SELECT 1 AS connection_test;" 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Connection failed:" -ForegroundColor Red
        Write-Host $testResult -ForegroundColor Red
        Write-Host "Please verify:" -ForegroundColor Yellow
        Write-Host ("1. PostgreSQL service is running (trying to connect to {0}:{1}" -f $PgHost, $PgPort)
        Write-Host "2. Username/password are correct"
        Write-Host "3. Your pg_hba.conf allows password authentication"
        exit 1
    }

    Write-Host "Creating user $NewDbUser..." -ForegroundColor Cyan
    & $psqlExe -U $RootUser -h $PgHost -p $PgPort -c "CREATE USER $NewDbUser WITH PASSWORD '$NewDbPassword';"
    if ($LASTEXITCODE -ne 0) { throw "Failed to create user" }
    
    Write-Host "Creating database $NewDbName..." -ForegroundColor Cyan
    & $psqlExe -U $RootUser -h $PgHost -p $PgPort -c "CREATE DATABASE $NewDbName WITH OWNER = $NewDbUser ENCODING = 'UTF8';"
    if ($LASTEXITCODE -ne 0) { throw "Failed to create database" }
    
    Write-Host "Granting privileges..." -ForegroundColor Cyan
    & $psqlExe -U $RootUser -h $PgHost -p $PgPort -c "GRANT ALL PRIVILEGES ON DATABASE $NewDbName TO $NewDbUser;"
    if ($LASTEXITCODE -ne 0) { throw "Failed to grant privileges" }
    
    Write-Host "`nSuccessfully created:" -ForegroundColor Green
    Write-Host "Database: $NewDbName" -ForegroundColor Yellow
    Write-Host "User: $NewDbUser" -ForegroundColor Yellow
    Write-Host ("Host: {0}:{1}" -f $PgHost, $PgPort) -ForegroundColor Yellow
}
catch {
    Write-Host "Error: $_" -ForegroundColor Red
    exit 1
}
finally {
    # Clear the password from environment
    Remove-Item Env:\PGPASSWORD
}