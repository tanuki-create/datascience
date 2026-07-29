#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Classify disk usage rows and write a status report.
.DESCRIPTION
    Demonstrates splitting a PowerShell script into single-responsibility
    functions: Get-UsageRows / Write-Report (side effects) and
    Get-DiskStatus / Get-SummaryExitCode (pure functions).
    Run with -TestMode to dot-source only the function definitions,
    e.g. from a Pester test, without executing the main body.
#>
param(
    [string]$InputPath,
    [string]$OutputPath,
    [double]$Warn = 80,
    [double]$Crit = 90,
    [switch]$TestMode
)

$ErrorActionPreference = 'Stop'

function Get-DiskStatus {
    # Pure function: no I/O, deterministic output.
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][double]$UsagePercent,
        [Parameter(Mandatory = $true)][double]$Warn,
        [Parameter(Mandatory = $true)][double]$Crit
    )
    if ($UsagePercent -ge $Crit) { return 'CRITICAL' }
    if ($UsagePercent -ge $Warn) { return 'WARNING' }
    return 'OK'
}

function Get-SummaryExitCode {
    # Pure function.
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][string[]]$Statuses)
    if ($Statuses -contains 'CRITICAL') { return 3 }
    return 0
}

function Get-UsageRows {
    # Side effect: reads a file from disk.
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][string]$Path)

    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "usage file not found: $Path"
    }
    Import-Csv -LiteralPath $Path
}

function Write-Report {
    # Side effect: writes a file to disk.
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][object[]]$Rows
    )
    $parent = Split-Path -Parent $Path
    if ($parent -and -not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }
    $Rows | Export-Csv -LiteralPath $Path -NoTypeInformation -Encoding utf8
}

if ($TestMode) {
    return
}

if ([string]::IsNullOrWhiteSpace($InputPath) -or [string]::IsNullOrWhiteSpace($OutputPath)) {
    [Console]::Error.WriteLine('-InputPath and -OutputPath are required')
    exit 1
}

if ($Warn -gt $Crit) {
    [Console]::Error.WriteLine('-Warn must be <= -Crit')
    exit 1
}

try {
    $usages = Get-UsageRows -Path $InputPath
}
catch {
    [Console]::Error.WriteLine($_.Exception.Message)
    exit 1
}

$rows = @()
$statuses = @()
foreach ($item in $usages) {
    $usagePercent = [double]$item.usage_percent
    $status = Get-DiskStatus -UsagePercent $usagePercent -Warn $Warn -Crit $Crit
    $statuses += $status
    $rows += [pscustomobject]@{
        host           = $item.host
        usage_percent  = $usagePercent
        status         = $status
    }
}

Write-Report -Path $OutputPath -Rows $rows
[Console]::Error.WriteLine("wrote $($rows.Count) rows to $OutputPath")

exit (Get-SummaryExitCode -Statuses $statuses)
