#!/usr/bin/env pwsh
<#
.SYNOPSIS
    ディスク使用率を ok/warning/critical に分類する（第13章のテスト対象）。

.DESCRIPTION
    ローカルディスクの使用率を取得し、閾値に基づいて分類してJSONで出力する。
    Get-LocalDiskUsage と Invoke-DiskClassification を分離しているため、
    Pesterのテストでは Get-LocalDiskUsage をモックし、実機のディスク構成に
    依存せずに分類ロジックを検証できる。

.PARAMETER WarnPercent
    warning とみなす使用率のしきい値（既定: 80）。

.PARAMETER CritPercent
    critical とみなす使用率のしきい値（既定: 90）。
#>
[CmdletBinding()]
param(
    [double]$WarnPercent = 80,
    [double]$CritPercent = 90
)

$ErrorActionPreference = 'Stop'

$Script:EXIT_OK = 0
$Script:EXIT_USAGE = 1
$Script:EXIT_CRITICAL = 3

function Get-DiskStatus {
    <#
    .SYNOPSIS
        使用率を ok/warning/critical に分類する。境界値は「以上」で次の段階に上がる。
    #>
    param(
        [Parameter(Mandatory = $true)][double]$UsedPercent,
        [Parameter(Mandatory = $true)][double]$WarnPercent,
        [Parameter(Mandatory = $true)][double]$CritPercent
    )

    if ($WarnPercent -gt $CritPercent) {
        throw "warn_percent ($WarnPercent) must be <= crit_percent ($CritPercent)"
    }
    if ($UsedPercent -lt 0 -or $UsedPercent -gt 100) {
        throw "used_percent out of range: $UsedPercent"
    }

    if ($UsedPercent -ge $CritPercent) {
        return 'critical'
    }
    elseif ($UsedPercent -ge $WarnPercent) {
        return 'warning'
    }
    else {
        return 'ok'
    }
}

function Get-LocalDiskUsage {
    <#
    .SYNOPSIS
        ローカルの固定ディスクの使用率を取得する。
    .DESCRIPTION
        Get-CimInstanceのラッパーであり、単体テストではこの関数をモックすることで
        実機のディスク構成に依存しないテストにする（第13章のモックの考え方）。
    #>
    Get-CimInstance -ClassName Win32_LogicalDisk -Filter 'DriveType=3' |
        ForEach-Object {
            $total = $_.Size
            $free = $_.FreeSpace
            if (-not $total) {
                return
            }
            $usedPercent = [Math]::Round((($total - $free) / $total) * 100, 1)
            [pscustomobject]@{
                MountPoint  = $_.DeviceID
                UsedPercent = $usedPercent
            }
        }
}

function Invoke-DiskClassification {
    <#
    .SYNOPSIS
        複数のディスク使用率をまとめて分類し、最悪ステータスも返す。
    #>
    param(
        [Parameter(Mandatory = $true)][object[]]$Usages,
        [double]$WarnPercent = 80,
        [double]$CritPercent = 90
    )

    $results = @()
    $worst = 'ok'
    $severity = @{ ok = 0; warning = 1; critical = 2 }

    foreach ($usage in $Usages) {
        $status = Get-DiskStatus -UsedPercent $usage.UsedPercent -WarnPercent $WarnPercent -CritPercent $CritPercent
        $results += [pscustomobject]@{
            MountPoint  = $usage.MountPoint
            UsedPercent = $usage.UsedPercent
            Status      = $status
        }
        if ($severity[$status] -gt $severity[$worst]) {
            $worst = $status
        }
    }

    [pscustomobject]@{
        Results = $results
        Worst   = $worst
    }
}

function Invoke-Main {
    <#
    .SYNOPSIS
        ディスク使用率を取得・分類し、JSONを出力して終了コードを返す。
    #>
    param(
        [double]$WarnPercent = 80,
        [double]$CritPercent = 90
    )

    try {
        $usages = Get-LocalDiskUsage
        $report = Invoke-DiskClassification -Usages $usages -WarnPercent $WarnPercent -CritPercent $CritPercent
    }
    catch {
        [Console]::Error.WriteLine("error: $($_.Exception.Message)")
        return $Script:EXIT_USAGE
    }

    $report | ConvertTo-Json -Depth 4

    if ($report.Worst -eq 'critical') {
        return $Script:EXIT_CRITICAL
    }
    return $Script:EXIT_OK
}

# ドットソース（. ./13_classify_disk.ps1）された場合は関数定義だけを行い、
# 直接実行された場合のみ Invoke-Main を呼んで exit する。
# テストからは前者の方法で関数だけを読み込む（第13章のテスト方法を参照）。
if ($MyInvocation.InvocationName -ne '.') {
    exit (Invoke-Main -WarnPercent $WarnPercent -CritPercent $CritPercent)
}
