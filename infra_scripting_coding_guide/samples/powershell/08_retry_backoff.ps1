#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Ping hosts with retry and exponential backoff.
.DESCRIPTION
    Distinguishes a permanent failure (ping command missing) from a
    retryable failure (no reply, timeout), reports partial success, and
    writes a CSV with per-host attempt counts.
#>
param(
    [Parameter(Mandatory = $true)]
    [string]$HostsFile,

    [Parameter(Mandatory = $true)]
    [string]$Report,

    [string]$Command = 'ping',
    [int]$TimeoutSeconds = 2,
    [int]$MaxAttempts = 4,
    [double]$BaseDelaySeconds = 0.5
)

$ErrorActionPreference = 'Stop'

$EXIT_OK = 0
$EXIT_USAGE = 1
$EXIT_RUNTIME = 2

class PermanentHealthCheckError : System.Exception {
    PermanentHealthCheckError([string]$Message) : base($Message) {}
}

class RetryableHealthCheckError : System.Exception {
    RetryableHealthCheckError([string]$Message) : base($Message) {}
}

function Invoke-HealthCheckOnce {
    param(
        [Parameter(Mandatory = $true)][string]$TargetHost,
        [Parameter(Mandatory = $true)][string]$Command,
        [Parameter(Mandatory = $true)][int]$TimeoutSeconds
    )

    if (-not (Get-Command -Name $Command -ErrorAction SilentlyContinue)) {
        throw [PermanentHealthCheckError]::new("command not found: $Command")
    }

    $ok = Test-Connection -TargetName $TargetHost -Count 1 -TimeoutSeconds $TimeoutSeconds -Quiet -ErrorAction SilentlyContinue
    if (-not $ok) {
        throw [RetryableHealthCheckError]::new("no reply from $TargetHost")
    }
}

function Invoke-WithRetry {
    param(
        [Parameter(Mandatory = $true)][scriptblock]$Action,
        [int]$MaxAttempts = 4,
        [double]$BaseDelaySeconds = 0.5
    )

    $attempt = 0
    while ($true) {
        $attempt++
        try {
            & $Action
            return [pscustomobject]@{ Ok = $true; Attempts = $attempt; Detail = 'ok' }
        }
        catch [PermanentHealthCheckError] {
            return [pscustomobject]@{ Ok = $false; Attempts = $attempt; Detail = $_.Exception.Message }
        }
        catch [RetryableHealthCheckError] {
            if ($attempt -ge $MaxAttempts) {
                return [pscustomobject]@{ Ok = $false; Attempts = $attempt; Detail = $_.Exception.Message }
            }
            $delay = $BaseDelaySeconds * [Math]::Pow(2, $attempt - 1)
            [Console]::Error.WriteLine("attempt $attempt/$MaxAttempts failed: $($_.Exception.Message); retrying in ${delay}s")
            Start-Sleep -Seconds $delay
        }
    }
}

if (-not (Test-Path -LiteralPath $HostsFile -PathType Leaf)) {
    [Console]::Error.WriteLine("hosts file not found: $HostsFile")
    exit $EXIT_USAGE
}

$hosts = Get-Content -LiteralPath $HostsFile |
    ForEach-Object { $_.Trim() } |
    Where-Object { $_ -and -not $_.StartsWith('#') }

$reportDir = Split-Path -Parent $Report
if ($reportDir -and -not (Test-Path -LiteralPath $reportDir)) {
    New-Item -ItemType Directory -Path $reportDir -Force | Out-Null
}

$rows = @()
$hadFailure = $false

foreach ($targetHost in $hosts) {
    $result = Invoke-WithRetry -MaxAttempts $MaxAttempts -BaseDelaySeconds $BaseDelaySeconds -Action {
        Invoke-HealthCheckOnce -TargetHost $targetHost -Command $Command -TimeoutSeconds $TimeoutSeconds
    }

    $rows += [pscustomobject]@{
        host     = $targetHost
        ok       = $result.Ok
        attempts = $result.Attempts
        detail   = $result.Detail
    }

    if (-not $result.Ok) {
        [Console]::Error.WriteLine("host=$targetHost failed after $($result.Attempts) attempts: $($result.Detail)")
        $hadFailure = $true
    }
}

$rows | Export-Csv -LiteralPath $Report -NoTypeInformation -Encoding utf8
[Console]::Error.WriteLine("wrote report to $Report")

if ($hadFailure) {
    exit $EXIT_RUNTIME
}
exit $EXIT_OK
