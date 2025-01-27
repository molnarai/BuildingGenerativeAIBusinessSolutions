function Write-Banner {
    Write-Host @"
  ____                 _     ____                 _                                  _    
 |  _ \ ___  __ _  ___| |_  |  _ \  _____   _____| | ___  _ __  _ __ ___   ___ _ __ | |_  
 | |_) / _ \/ _` |/ __| __| | | | |/ _ \ \ / / _ \ |/ _ \| '_ \| '_ ` _ \ / _ \ '_ \| __| 
 |  _ <  __/ (_| | (__| |_  | |_| |  __/\ V /  __/ | (_) | |_) | | | | | |  __/ | | | |_  
 |_| \_\___|\__,_|\___|\__| |____/ \___| \_/ \___|_|\___/| .__/|_| |_| |_|\___|_| |_|\__| 
                                                         |_|                                                                                                                    
Locally run React Development Environment
"@
}

# Check if podman or docker command is installed, define variable CONTAINERCMD
$CONTAINER_CMD = if (Get-Command podman -ErrorAction SilentlyContinue) {
    Write-Host "podman found"
    "podman"
} elseif (Get-Command docker -ErrorAction SilentlyContinue) {
    Write-Host "docker found"
    "docker"
} else {
    Write-Host "Neither podman nor docker command found. Please install one of them."
    exit 1
}

$FRONTEND_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$APP_NAME = [System.IO.Path]::GetFileNameWithoutExtension($MyInvocation.MyCommand.Name)
$CONTAINER_NAME = "local/$($env:USERNAME.ToLower())/$APP_NAME"
Write-Host "Container name: $CONTAINER_NAME"

$LOCAL_PORT = 3000

$CMD = if ($args.Count -eq 0) { "help" } else { $args[0] }

if (-not (Test-Path "src/$APP_NAME/.env")) {
    Write-Host "Creating .env file"
    @"
REACT_APP_OLLAMA_BASE_URL=$env:OLLAMA_BASE_URL
REACT_APP_AI_APPLICATION_BASE_URL=$env:AI_APPLICATION_BASE_URL
REACT_APP_AI_APPLICATION_NAME=$($env:AI_APPLICATION_NAME -or $APP_NAME)
"@ | Set-Content "src/$APP_NAME/.env"
}

switch ($CMD) {
    "install" {
        Write-Host "Building container"
        & $CONTAINER_CMD build -t $CONTAINER_NAME .
    }
    "run" {
        Write-Host "Running container"
        $runArgs = $args[1..($args.Length-1)]
        & $CONTAINER_CMD run -it --rm `
            -p "${LOCAL_PORT}:3000" `
            -v "${FRONTEND_DIR}/src:/app/src" `
            -w /app/src/$APP_NAME `
            $CONTAINER_NAME $runArgs
    }
    "create" {
        if (Test-Path $APP_NAME) {
            Write-Host "Directory $APP_NAME already exists. Please remove it first."
            exit 1
        }
        Write-Host "Creating Application"
        & $CONTAINER_CMD run -it --rm `
            -v "${FRONTEND_DIR}/src:/app/src" `
            -w /app/src `
            $CONTAINER_NAME npx create-react-app $APP_NAME
    }
    "build" {
        Write-Host "Build static React app"
        & $CONTAINER_CMD run --rm `
            -v "${FRONTEND_DIR}/src:/app/src" `
            -w /app/src/$APP_NAME `
            $CONTAINER_NAME npm install
        & $CONTAINER_CMD run --rm `
            -v "${FRONTEND_DIR}/src:/app/src" `
            -w /app/src/$APP_NAME `
            $CONTAINER_NAME npm run build 
    }
    "start" {
        Write-Host "Starting container"
        & $CONTAINER_CMD run -it --rm `
            -p "${LOCAL_PORT}:3000" `
            -v "${FRONTEND_DIR}/src:/app/src" `
            -w /app/src/$APP_NAME `
            $CONTAINER_NAME npm start 
    }
    default {
        Write-Host @"
Usage: $($MyInvocation.MyCommand.Name) [install|run|create|build|start]

install: Build the container image
run:     Run the container in interactive mode
create:  Create a new React application with the name $APP_NAME
build:   Build the React application
start:   Start the React application in development mode
"@
        exit 1
    }
}

Write-Host "done."
