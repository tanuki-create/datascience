#!/usr/bin/env pwsh
param(
    [Parameter(Mandatory = $true)]
    [string]$HostsFile
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $HostsFile -PathType Leaf)) {
    [Console]::Error.WriteLine("hosts file not found: $HostsFile")
    exit 2
}

$hosts = @()
$lineNo = 0
foreach ($raw in Get-Content -LiteralPath $HostsFile) {
    $lineNo++
    $line = $raw.Trim()
    if ([string]::IsNullOrWhiteSpace($line)) { continue }
    if ($line.StartsWith('#')) { continue }
    if ($line -match '\s') {
        [Console]::Error.WriteLine("invalid host at line ${lineNo}: contains whitespace")
        exit 2
    }
    $hosts += $line
}

[Console]::Error.WriteLine("loaded $($hosts.Count) hosts")
Write-Output $hosts.Count
exit 0
