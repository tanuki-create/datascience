#!/usr/bin/env pwsh
<#
opsctl service-check（PowerShell版）: Windowsサービスの稼働状態を
確認する。

既定では状態確認のみ行う。-RestartOnFailure を付けると、停止している
サービスの再起動を試みる。

警告: -RestartOnFailure はサービスを再起動する破壊的操作である。
本番相当のホストに対して、変更管理の承認なしに使わないこと。
まず -DryRun で再起動の予定を確認すること。
#>
param(
    [Parameter(Mandatory = $true)]
    [string[]]$ServiceName,
    [string]$ReportPath = 'work/reports/service_check.csv',
    [switch]$RestartOnFailure,
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

function Write-Log {
    param([string]$Level, [string]$Message)
    $ts = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
    [Console]::Error.WriteLine("$ts $Level $Message")
}

$parent = Split-Path -Parent $ReportPath
if ($parent -and -not (Test-Path -LiteralPath $parent)) {
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
}

$rows = @()
$hadFailure = $false

foreach ($name in $ServiceName) {
    $svc = Get-Service -Name $name -ErrorAction SilentlyContinue
    if (-not $svc) {
        Write-Log 'ERROR' "service not found: $name"
        $rows += [pscustomobject]@{ service = $name; status = 'not_found'; action = 'none' }
        $hadFailure = $true
        continue
    }

    if ($svc.Status -eq 'Running') {
        Write-Log 'INFO' "service=$name status=Running"
        $rows += [pscustomobject]@{ service = $name; status = 'Running'; action = 'none' }
        continue
    }

    $hadFailure = $true
    $action = 'none'
    if ($RestartOnFailure) {
        if ($DryRun) {
            Write-Log 'WARNING' "dry-run: would restart stopped service=$name"
            $action = 'dry-run-restart'
        } else {
            Write-Log 'WARNING' "service=$name status=$($svc.Status); attempting restart"
            try {
                Restart-Service -Name $name -ErrorAction Stop
                $action = 'restarted'
                Write-Log 'INFO' "service=$name restarted successfully"
            } catch {
                $action = 'restart-failed'
                Write-Log 'ERROR' "failed to restart service=${name}: $($_.Exception.Message)"
            }
        }
    } else {
        Write-Log 'WARNING' "service=$name status=$($svc.Status)"
    }
    $rows += [pscustomobject]@{ service = $name; status = $svc.Status; action = $action }
}

$rows | Export-Csv -LiteralPath $ReportPath -NoTypeInformation -Encoding utf8
Write-Log 'INFO' "wrote report to $ReportPath"

if ($hadFailure) { exit 2 }
exit 0
