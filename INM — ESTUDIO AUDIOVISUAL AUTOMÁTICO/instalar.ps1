# Instalador del Estudio INM para Windows (PowerShell).
# Uso: clic derecho > "Ejecutar con PowerShell", o desde Claude Code/Cowork:
#   powershell -ExecutionPolicy Bypass -File instalar.ps1
# Pide confirmación antes de instalar programas del sistema (FFmpeg, Node, Python, Git) con winget.
$ErrorActionPreference = "Stop"
$Raiz = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Raiz
Write-Host "== Estudio INM: comprobando programas ==" -ForegroundColor Cyan

function Falta($cmd) { -not (Get-Command $cmd -ErrorAction SilentlyContinue) }
$paquetes = @()
if (Falta "ffmpeg") { $paquetes += @{id="Gyan.FFmpeg"; nombre="FFmpeg"} }
if (Falta "node")   { $paquetes += @{id="OpenJS.NodeJS.LTS"; nombre="Node.js LTS (22 o superior)"} }
if ((Falta "python") -and (Falta "py")) { $paquetes += @{id="Python.Python.3.12"; nombre="Python 3.12"} }
if (Falta "git")    { $paquetes += @{id="Git.Git"; nombre="Git"} }

if ($paquetes.Count -gt 0) {
  Write-Host "Faltan: $($paquetes.nombre -join ', ')"
  $r = Read-Host "¿Instalarlos ahora con winget (gratuitos, puede pedir permiso de administrador)? (s/n)"
  if ($r -ne "s") { Write-Host "Cancelado. Instálalos y vuelve a ejecutar."; exit 1 }
  foreach ($p in $paquetes) { winget install --id $p.id -e --accept-package-agreements --accept-source-agreements }
  Write-Host "Cierra esta ventana y vuelve a ejecutar el instalador para que Windows vea los programas nuevos." -ForegroundColor Yellow
  exit 0
}

$py = if (Get-Command py -ErrorAction SilentlyContinue) { "py" } else { "python" }
if (-not (Test-Path "_HERRAMIENTAS\venv")) { & $py -m venv _HERRAMIENTAS\venv }
& _HERRAMIENTAS\venv\Scripts\python.exe -m pip install --upgrade pip
& _HERRAMIENTAS\venv\Scripts\python.exe -m pip install -r _HERRAMIENTAS\requirements.txt
& _HERRAMIENTAS\venv\Scripts\python.exe 12_AUTOMATIZACIONES\sfx.py
& _HERRAMIENTAS\venv\Scripts\python.exe 12_AUTOMATIZACIONES\preparar.py
Write-Host "== Prueba real de 5 segundos ==" -ForegroundColor Cyan
& _HERRAMIENTAS\venv\Scripts\python.exe 12_AUTOMATIZACIONES\prueba_5s.py
Write-Host "Listo. Lee COMO-FUNCIONA.md" -ForegroundColor Green
