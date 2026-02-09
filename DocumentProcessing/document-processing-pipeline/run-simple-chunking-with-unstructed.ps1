param(
	[switch]$Help,
	[switch]$ByTitle,
	[switch]$Basic,
	[int]$MaxChunkSize = 1000,
	[int]$MaxChunkOverlap = 0
)

@'
██╗   ██╗███╗   ██╗███████╗████████╗██████╗ ██╗   ██╗ ██████╗████████╗██╗   ██╗██████╗ ███████╗██████╗ 
██║   ██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██║   ██║██╔════╝╚══██╔══╝██║   ██║██╔══██╗██╔════╝██╔══██╗
██║   ██║██╔██╗ ██║███████╗   ██║   ██████╔╝██║   ██║██║        ██║   ██║   ██║██████╔╝█████╗  ██║  ██║
██║   ██║██║╚██╗██║╚════██║   ██║   ██╔══██╗██║   ██║██║        ██║   ██║   ██║██╔══██╗██╔══╝  ██║  ██║
╚██████╔╝██║ ╚████║███████║   ██║   ██║  ██║╚██████╔╝╚██████╗   ██║   ╚██████╔╝██║  ██║███████╗██████╔╝
 ╚═════╝ ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝  ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═════╝ 
                                                                                                       
This script is for running the simple PDF extraction service using Docker Compose.
'@ | Write-Host

if ($Help) {
	@"
Usage:
	.\run-simple-chunking-with-unstructed.ps1 [options]

Options:
	-ByTitle           Use by_title chunking strategy
	-Basic             Use basic chunking strategy
	-MaxChunkSize      Maximum chunk size (default: 1000)
	-MaxChunkOverlap   Maximum chunk overlap (default: 0)
	-Help              Show this help message

Examples:
	.\run-simple-chunking-with-unstructed.ps1
	.\run-simple-chunking-with-unstructed.ps1 -ByTitle
	.\run-simple-chunking-with-unstructed.ps1 -Basic
	.\run-simple-chunking-with-unstructed.ps1 -ByTitle -MaxChunkSize 1200 -MaxChunkOverlap 100
"@ | Write-Host
	exit 0
}

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
Push-Location "simple-chunking-with-unstructured"
try {
	& $composeCmd build
	$pythonArgs = @()
	if ($ByTitle) {
		$pythonArgs += "--by-title"
	}
	if ($Basic) {
		$pythonArgs += "--basic"
	}
	$pythonArgs += "--max-chunk-size"
	$pythonArgs += $MaxChunkSize
	$pythonArgs += "--max-chunk-overlap"
	$pythonArgs += $MaxChunkOverlap

	& $composeCmd run --rm chunking-with-unstructured /usr/bin/python ./src/main.py @pythonArgs
} finally {
	Pop-Location
}
