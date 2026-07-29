#!/usr/bin/env pwsh
<#
opsctl user-audit: ローカルユーザーアカウントを棚卸しし、リスクのある
アカウントを検出する。

対象はWindowsのローカルアカウント（Get-LocalUser）である。
LinuxやmacOSの/etc/passwd相当を棚卸しする場合は、
samples/bash/15_user_audit.sh を使うこと。

読み取り専用の監査であり、アカウントの変更は一切行わない。
それでも、対象システムによっては実行に管理者権限が必要な場合があるため、
実行前に必要な権限を確認すること。
#>
param(
    [int]$InactiveDaysWarn = 90,
    [string[]]$ExcludedAccounts = @('DefaultAccount', 'Guest', 'WDAGUtilityAccount', 'defaultuser0'),
    [string]$ReportPath = 'work/reports/user_audit.csv',
    [switch]$DryRun,
    [switch]$Verbose
)

$ErrorActionPreference = 'Stop'

$ExitOk = 0
$ExitUsage = 1
$ExitRuntime = 2
$ExitCritical = 3

function Write-Log {
    param([string]$Level, [string]$Message)
    if ($Level -eq 'DEBUG' -and -not $Verbose) { return }
    $ts = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
    [Console]::Error.WriteLine("$ts $Level $Message")
}

function Get-AccountFindings {
    param(
        [Parameter(Mandatory = $true)][object]$User,
        [Parameter(Mandatory = $true)][int]$InactiveDaysWarn
    )
    $findings = @()
    if (-not $User.PasswordRequired) {
        $findings += 'no_password_required'
    }
    if ($User.PasswordRequired -and $null -eq $User.PasswordExpires) {
        $findings += 'password_never_expires'
    }
    $lastLogon = $User.LastLogon
    if (-not $lastLogon) {
        $findings += 'never_logged_on'
    } else {
        $idleDays = (New-TimeSpan -Start $lastLogon -End (Get-Date)).Days
        if ($idleDays -ge $InactiveDaysWarn) {
            $findings += "inactive_${idleDays}d"
        }
    }
    return $findings
}

if (-not (Get-Command Get-LocalUser -ErrorAction SilentlyContinue)) {
    Write-Log 'ERROR' 'Get-LocalUser is not available on this platform (Windows only). Use samples/bash/15_user_audit.sh on Linux/macOS.'
    exit $ExitUsage
}

try {
    $allUsers = Get-LocalUser
} catch {
    Write-Log 'ERROR' "failed to enumerate local users: $($_.Exception.Message)"
    exit $ExitRuntime
}

$targetUsers = $allUsers | Where-Object { $_.Enabled -and ($ExcludedAccounts -notcontains $_.Name) }
Write-Log 'INFO' "auditing $($targetUsers.Count) enabled account(s) out of $($allUsers.Count) total"

if ($DryRun) {
    foreach ($u in $targetUsers) {
        Write-Log 'INFO' "dry-run: would audit account=$($u.Name)"
    }
    exit $ExitOk
}

$rows = @()
$hadCritical = $false
$hadWarning = $false

foreach ($u in $targetUsers) {
    $findings = Get-AccountFindings -User $u -InactiveDaysWarn $InactiveDaysWarn
    if ($findings -contains 'no_password_required') {
        $hadCritical = $true
    } elseif ($findings.Count -gt 0) {
        $hadWarning = $true
    }
    Write-Log 'DEBUG' "account=$($u.Name) findings=$($findings -join ';')"
    $rows += [pscustomobject]@{
        name              = $u.Name
        enabled           = $u.Enabled
        password_required = $u.PasswordRequired
        password_expires  = $u.PasswordExpires
        last_logon        = $u.LastLogon
        findings          = ($findings -join ';')
    }
}

$parent = Split-Path -Parent $ReportPath
if ($parent -and -not (Test-Path -LiteralPath $parent)) {
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
}
$rows | Export-Csv -LiteralPath $ReportPath -NoTypeInformation -Encoding utf8
Write-Log 'INFO' "wrote report to $ReportPath"

if ($hadCritical) { exit $ExitCritical }
if ($hadWarning) { exit $ExitRuntime }
exit $ExitOk
