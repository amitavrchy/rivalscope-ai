$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot
$env:NODE_USE_SYSTEM_CA = '1'
& docker compose up -d --wait postgres redis mailpit
if ($LASTEXITCODE -ne 0) { throw 'Docker services failed to start. Start Docker Desktop and try again.' }
& npm --prefix rivalscope-backend run build
if ($LASTEXITCODE -ne 0) { throw 'API build failed.' }
$artifactPath = Join-Path $projectRoot 'artifacts'
New-Item -ItemType Directory -Path $artifactPath -Force | Out-Null
$nodeBinary = (Get-Command node).Source
$processes = @{}
foreach ($service in @(
  @{ Name='api'; Port=4000; Directory='rivalscope-backend'; Arguments=@('--use-system-ca','dist/main.js') },
  @{ Name='web'; Port=3000; Directory='rivalscope-frontend'; Arguments=@('node_modules/next/dist/bin/next','dev','--hostname','0.0.0.0') },
  @{ Name='worker'; Port=0; Directory='rivalscope-backend'; Arguments=@('--use-system-ca','dist/worker.js') }
)) {
  if ($service.Port -gt 0) {
    $listener = Get-NetTCPConnection -State Listen -LocalPort $service.Port -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($listener) { $processes[$service.Name] = $listener.OwningProcess; continue }
  } else {
    $workerRecord = Join-Path $artifactPath 'worker-process.json'
    if (Test-Path -LiteralPath $workerRecord) {
      $saved = Get-Content -Raw -LiteralPath $workerRecord | ConvertFrom-Json
      $existing = Get-Process -Id $saved.id -ErrorAction SilentlyContinue
      if ($existing -and $existing.StartTime.ToUniversalTime().ToString('o') -eq $saved.startedAt) { $processes.worker = $existing.Id; continue }
    }
  }
  $serviceProcess = Start-Process -FilePath $nodeBinary -ArgumentList $service.Arguments -WorkingDirectory (Join-Path $projectRoot $service.Directory) -WindowStyle Hidden -RedirectStandardOutput (Join-Path $artifactPath ($service.Name+'.log')) -RedirectStandardError (Join-Path $artifactPath ($service.Name+'-error.log')) -PassThru
  $processes[$service.Name] = $serviceProcess.Id
  if ($service.Name -eq 'worker') { @{ id=$serviceProcess.Id; startedAt=$serviceProcess.StartTime.ToUniversalTime().ToString('o') } | ConvertTo-Json | Set-Content -LiteralPath $workerRecord }
}
$processes | ConvertTo-Json
Write-Output 'App: http://localhost:3000'
Write-Output 'API: http://localhost:4000/api/health/ready'
Write-Output 'Email inbox: http://localhost:8025'
