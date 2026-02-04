#!/usr/bin/env pwsh

Write-Host @"
  _                           _              ___        
 | |    __ _ _   _ _ __   ___| |__    _ __  ( _ ) _ __  
 | |   / _`` | | | | '_ \ / __| '_ \  | '_ \ / _ \| '_ \ 
 | |__| (_| | |_| | | | | (__| | | | | | | | (_) | | | |
 |_____\__,_|\__,_|_| |_|\___|_| |_| |_| |_|\___/|_| |_|
                                                        
"@

param(
    [Parameter(Position=0)]
    [string]$Action = "help",
    
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$RemainingArgs
)

# Get script directory and construct paths
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$WorkDir = Join-Path (Split-Path -Parent $ScriptDir) "n8n-experiments-system-store" | Resolve-Path -ErrorAction SilentlyContinue
if (-not $WorkDir) {
    $WorkDir = Join-Path (Split-Path -Parent $ScriptDir) "n8n-experiments-system-store"
}
$DataDir = Join-Path (Split-Path -Parent $ScriptDir) "n8n-experiments-data" | Resolve-Path -ErrorAction SilentlyContinue
if (-not $DataDir) {
    $DataDir = Join-Path (Split-Path -Parent $ScriptDir) "n8n-experiments-data"
}

Write-Host "Working directory: $WorkDir"
New-Item -ItemType Directory -Force -Path $WorkDir | Out-Null

$BasePort = 23010
$ServerIp = 'localhost'
$ContainerName = "$env:USERNAME-n8n-experiments"

# Determine container runtime
$Runtime = $null
$RuntimeArgs = @()

if (Get-Command podman -ErrorAction SilentlyContinue) {
    $Runtime = "podman"
    if ($IsLinux -or $IsMacOS) {
        $Uid = id -u
        $Gid = id -g
        $RuntimeArgs = @("--userns=keep-id", "--user", "${Uid}:${Gid}")
    }
} elseif (Get-Command docker -ErrorAction SilentlyContinue) {
    $Runtime = "docker"
} else {
    Write-Error "Error: Neither podman nor docker is installed."
    exit 1
}

switch ($Action.ToLower()) {
    "start" {
        # Read admin password
        $PasswordFile = Join-Path $HOME ".secrets/n8n-experiments-passwd.txt"
        if (Test-Path $PasswordFile) {
            $AdminPassword = Get-Content $PasswordFile -Raw
            $AdminPassword = $AdminPassword.Trim()
        } else {
            Write-Error "Password file not found: $PasswordFile"
            exit 1
        }
        
        $ConsolePort = $BasePort
        
        # Create data and config directories
        New-Item -ItemType Directory -Force -Path "$WorkDir/data/vol" | Out-Null
        New-Item -ItemType Directory -Force -Path "$WorkDir/config/vol" | Out-Null
        New-Item -ItemType Directory -Force -Path "$WorkDir/logs/vol" | Out-Null
        
        # Build the command arguments
        $CmdArgs = @(
            "run", "-d", "--name", $ContainerName,
            "--restart", "unless-stopped",
            "-p", "${ConsolePort}:5678"
        )
        $CmdArgs += $RuntimeArgs
        $CmdArgs += @(
            "-v", "${WorkDir}/data/vol:/home/node/.n8n",
            "-v", "${WorkDir}/logs/vol:/logs",
            "-v", "${DataDir}:/data",
            "-e", "N8N_HOST=0.0.0.0",
            "-e", "N8N_PORT=5678",
            "-e", "N8N_BASIC_AUTH_ACTIVE=true",
            "-e", "N8N_BASIC_AUTH_USER=admin",
            "-e", "N8N_BASIC_AUTH_PASSWORD=${AdminPassword}",
            "-e", "N8N_USER_MANAGEMENT_DISABLED=true",
            "-e", "N8N_DIAGNOSTICS_ENABLED=false",
            "-e", "N8N_VERSION_NOTIFICATIONS_ENABLED=false",
            "-e", "N8N_TEMPLATES_ENABLED=false",
            "-e", "N8N_ONBOARDING_FLOW_DISABLED=true",
            "-e", "N8N_PERSONALIZATION_ENABLED=false",
            "-e", "N8N_SECURE_COOKIE=false",
            "-e", "CODE_ENABLE_STDOUT=true",
            "-e", "N8N_LOG_FILE=/logs/${ContainerName}.log",
            "-e", "N8N_LOG_LEVEL=debug",
            "-e", "WEBHOOK_URL=http://${ServerIp}:${ConsolePort}",
            "docker.io/n8nio/n8n:latest"
        )
        
        & $Runtime $CmdArgs
        & $Runtime ps
        
        # Open browser (cross-platform)
        $Url = "http://localhost:${ConsolePort}/"
        if ($IsMacOS) {
            open $Url
        } elseif ($IsWindows) {
            Start-Process $Url
        } elseif ($IsLinux) {
            if (Get-Command xdg-open -ErrorAction SilentlyContinue) {
                xdg-open $Url
            }
        }
    }
    
    "stop" {
        & $Runtime stop $ContainerName
        & $Runtime rm $ContainerName
    }
    
    "logs" {
        & $Runtime logs -f $ContainerName
    }
    
    "exec" {
        if ($RemainingArgs.Count -gt 0) {
            & $Runtime exec -it $ContainerName $RemainingArgs
        } else {
            & $Runtime exec -it $ContainerName /bin/sh
        }
    }
    
    default {
        Write-Host "Usage: $($MyInvocation.MyCommand.Name) {start|stop|logs|exec|help}"
        Write-Host "  start   - Start the n8n containers"
        Write-Host "  stop    - Stop and remove the n8n containers"
        Write-Host "  logs    - View the logs of the containers"
        Write-Host "  exec    - Execute a command in the running containers"
        Write-Host "  help    - Display this help message"
    }
}
