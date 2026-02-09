@'
███████╗██╗███╗   ███╗██████╗ ██╗     ███████╗    ██████╗ ██████╗ ███████╗
██╔════╝██║████╗ ████║██╔══██╗██║     ██╔════╝    ██╔══██╗██╔══██╗██╔════╝
███████╗██║██╔████╔██║██████╔╝██║     █████╗      ██████╔╝██║  ██║█████╗
╚════██║██║██║╚██╔╝██║██╔═══╝ ██║     ██╔══╝      ██╔═══╝ ██║  ██║██╔══╝
███████║██║██║ ╚═╝ ██║██║     ███████╗███████╗    ██║     ██████╔╝██║
╚══════╝╚═╝╚═╝     ╚═╝╚═╝     ╚══════╝╚══════╝    ╚═╝     ╚═════╝ ╚═╝

███████╗██╗  ██╗████████╗██████╗  █████╗  ██████╗████████╗██╗ ██████╗ ███╗   ██╗
██╔════╝╚██╗██╔╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║
█████╗   ╚███╔╝    ██║   ██████╔╝███████║██║        ██║   ██║██║   ██║██╔██╗ ██║
██╔══╝   ██╔██╗    ██║   ██╔══██╗██╔══██║██║        ██║   ██║██║   ██║██║╚██╗██║
███████╗██╔╝ ██╗   ██║   ██║  ██║██║  ██║╚██████╗   ██║   ██║╚██████╔╝██║ ╚████║
╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝

This script is for running the simple PDF extraction service using Docker Compose.
'@ | Write-Host

$dockerCmd = $null
if (Get-Command docker -ErrorAction SilentlyContinue) {
	Write-Host "Using Docker"
	$dockerCmd = "docker"
} elseif (Get-Command podman -ErrorAction SilentlyContinue) {
	Write-Host "Using Podman"
	$dockerCmd = "podman"
} else {
	Write-Host "Neither Docker nor Podman is installed. Please install one of them to proceed."
	exit 1
}

$composeCmd = "${dockerCmd}-compose"
Push-Location "simple-pdf-extraction"
try {
	& $composeCmd build
	& $composeCmd run --rm pdf-extractor ./run.sh
} finally {
	Pop-Location
}
