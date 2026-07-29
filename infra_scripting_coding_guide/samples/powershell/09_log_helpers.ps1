#!/usr/bin/env pwsh
# ログ用ヘルパー関数。ドット呼び出しで読み込む。
#   . ./samples/powershell/09_log_helpers.ps1
#   Write-Log -Level 'INFO' -Message 'starting'
#   Write-JsonLog -Level 'INFO' -Message 'starting' -RunId ([guid]::NewGuid().ToString())

function Write-Log {
    param(
        [Parameter(Mandatory = $true)][string]$Level,
        [Parameter(Mandatory = $true)][string]$Message
    )
    $ts = [DateTimeOffset]::UtcNow.ToString('o')
    [Console]::Error.WriteLine("$ts $Level $Message")
}

function Write-JsonLog {
    param(
        [Parameter(Mandatory = $true)][string]$Level,
        [Parameter(Mandatory = $true)][string]$Message,
        [Parameter(Mandatory = $true)][string]$RunId
    )
    [pscustomobject]@{
        ts      = [DateTimeOffset]::UtcNow.ToString('o')
        level   = $Level
        run_id  = $RunId
        event   = 'opsctl'
        message = $Message
    } | ConvertTo-Json -Compress | ForEach-Object { [Console]::Error.WriteLine($_) }
}

if ($MyInvocation.InvocationName -ne '.') {
    $runId = [guid]::NewGuid().ToString()
    Write-Log -Level 'INFO' -Message 'starting'
    Write-JsonLog -Level 'WARNING' -Message 'disk usage high: 85%' -RunId $runId
    Write-Log -Level 'INFO' -Message 'finished'
}
