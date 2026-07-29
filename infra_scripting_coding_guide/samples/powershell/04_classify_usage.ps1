#!/usr/bin/env pwsh
param(
    [Parameter(Mandatory = $true)]
    [double]$Usage,
    [double]$Warn = 80,
    [double]$Crit = 90
)

$ErrorActionPreference = 'Stop'

function Classify {
    param([double]$Usage, [double]$Warn, [double]$Crit)
    if ($Usage -lt 0 -or $Usage -gt 100) {
        throw 'usage must be between 0 and 100'
    }
    if ($Warn -lt 0 -or $Crit -lt 0 -or $Warn -gt 100 -or $Crit -gt 100) {
        throw 'thresholds must be between 0 and 100'
    }
    if ($Warn -gt $Crit) {
        throw 'warn must be <= crit'
    }
    if ($Usage -ge $Crit) { return 'CRITICAL' }
    if ($Usage -ge $Warn) { return 'WARNING' }
    return 'OK'
}

try {
    $status = Classify -Usage $Usage -Warn $Warn -Crit $Crit
} catch {
    [Console]::Error.WriteLine($_.Exception.Message)
    exit 1
}

Write-Output $status
if ($status -eq 'CRITICAL') {
    exit 3
}
exit 0
