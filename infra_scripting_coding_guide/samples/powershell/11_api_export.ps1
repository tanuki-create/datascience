#!/usr/bin/env pwsh
<#
ページ分割APIからホスト情報を取得し、CSVへ書き出す。

APIホストは example.invalid（実在しないドメイン）を既定にしている。
-DryRun で組み立てとロジックだけを確認するか、-BaseUrl で到達可能な
テスト用APIに向けること。
#>
param(
    [string]$BaseUrl = 'https://api.example.invalid',
    [Parameter(Mandatory = $true)]
    [string]$OutputPath,
    [int]$TimeoutSec = 10,
    [int]$MaxRetries = 3,
    [switch]$DryRun,
    [switch]$Verbose
)

$ErrorActionPreference = 'Stop'

function Write-Info {
    param([string]$Message)
    if (-not $Verbose) { return }
    [Console]::Error.WriteLine("DEBUG $Message")
}

function Get-WithRetry {
    param(
        [Parameter(Mandatory = $true)][string]$Uri,
        [Parameter(Mandatory = $true)][hashtable]$Headers,
        [int]$TimeoutSec,
        [int]$MaxRetries
    )
    $attempt = 0
    while ($true) {
        $attempt++
        try {
            return Invoke-RestMethod -Uri $Uri -Headers $Headers -TimeoutSec $TimeoutSec -Method Get
        }
        catch {
            $statusCode = $null
            if ($_.Exception.Response) {
                $statusCode = [int]$_.Exception.Response.StatusCode
            }
            $retryable = ($null -eq $statusCode) -or ($statusCode -eq 429) -or ($statusCode -ge 500)
            if (-not $retryable -or $attempt -gt $MaxRetries) {
                throw
            }
            $backoff = [Math]::Min([Math]::Pow(2, $attempt), 30)
            Write-Warning "request failed (attempt $attempt/$MaxRetries); retrying in ${backoff}s"
            Start-Sleep -Seconds $backoff
        }
    }
}

$token = $env:OPSCTL_API_TOKEN
if ([string]::IsNullOrWhiteSpace($token)) {
    [Console]::Error.WriteLine('OPSCTL_API_TOKEN is required')
    exit 1
}

if ($DryRun) {
    [Console]::Error.WriteLine("dry-run: would GET $BaseUrl/v1/hosts and write $OutputPath")
    exit 0
}

$headers = @{ Authorization = "Bearer $token"; Accept = 'application/json' }
$records = @()
$cursor = $null

do {
    $uri = "$BaseUrl/v1/hosts?limit=100"
    if ($cursor) { $uri += "&cursor=$cursor" }
    Write-Info "fetching $uri"
    $page = Get-WithRetry -Uri $uri -Headers $headers -TimeoutSec $TimeoutSec -MaxRetries $MaxRetries
    $records += $page.items
    $cursor = $page.next_cursor
} while ($cursor)

$records |
    Select-Object @{Name = 'host'; Expression = { $_.host } },
                  @{Name = 'status'; Expression = { $_.status } },
                  @{Name = 'last_seen'; Expression = { $_.last_seen } } |
    Export-Csv -LiteralPath $OutputPath -NoTypeInformation -Encoding utf8

[Console]::Error.WriteLine("wrote $($records.Count) records to $OutputPath")
exit 0
