#!/usr/bin/env pwsh
<#
opsctl disk-check（PowerShell版）: ローカルドライブのディスク使用率を
監視する。

読み取り専用の監視であり、破壊的操作は行わない。
PowerShell 7をLinux/macOSで使う場合、FileSystemプロバイダーの
Used/Freeプロパティが取得できないドライブがある。その場合は
samples/bash/15_disk_check.sh を使うこと。
#>
param(
    [string[]]$DriveLetter,
    [double]$Warn = 80,
    [double]$Crit = 90,
    [string]$ReportPath = 'work/reports/disk_check.csv',
    [switch]$DryRun,
    [switch]$Verbose
)

$ErrorActionPreference = 'Stop'

function Write-Log {
    param([string]$Level, [string]$Message)
    $ts = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
    [Console]::Error.WriteLine("$ts $Level $Message")
}

function Get-DiskStatus {
    param([double]$UsePercent, [double]$Warn, [double]$Crit)
    if ($UsePercent -ge $Crit) { return 'CRITICAL' }
    if ($UsePercent -ge $Warn) { return 'WARNING' }
    return 'OK'
}

if ($Warn -gt $Crit) {
    Write-Log 'ERROR' '-Warn must be <= -Crit'
    exit 1
}

if ($DriveLetter) {
    $names = $DriveLetter -replace ':', ''
    $drives = Get-PSDrive -Name $names -PSProvider FileSystem -ErrorAction SilentlyContinue
} else {
    $drives = Get-PSDrive -PSProvider FileSystem | Where-Object { $null -ne $_.Used -and $null -ne $_.Free }
}

if (-not $drives) {
    Write-Log 'ERROR' 'no target drives found'
    exit 1
}

if ($DryRun) {
    foreach ($d in $drives) {
        Write-Log 'INFO' "dry-run: would check $($d.Name): warn=$Warn crit=$Crit"
    }
    exit 0
}

$parent = Split-Path -Parent $ReportPath
if ($parent -and -not (Test-Path -LiteralPath $parent)) {
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
}

$rows = @()
$hadCritical = $false

foreach ($d in $drives) {
    $total = $d.Used + $d.Free
    if ($total -le 0) { continue }
    $usePercent = [Math]::Round(($d.Used / $total) * 100, 1)
    $status = Get-DiskStatus -UsePercent $usePercent -Warn $Warn -Crit $Crit
    if ($status -eq 'CRITICAL') { $hadCritical = $true }
    if ($Verbose -or $status -ne 'OK') {
        Write-Log 'INFO' "target=$($d.Name): use_percent=$usePercent status=$status"
    }
    $rows += [pscustomobject]@{
        target      = "$($d.Name):"
        use_percent = $usePercent
        status      = $status
    }
}

$rows | Export-Csv -LiteralPath $ReportPath -NoTypeInformation -Encoding utf8
Write-Log 'INFO' "wrote report to $ReportPath"

if ($hadCritical) { exit 3 }
exit 0
