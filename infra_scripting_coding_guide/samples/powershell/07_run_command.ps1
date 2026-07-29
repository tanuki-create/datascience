#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Run an external command safely: argument array, timeout, no
    Invoke-Expression.
.DESCRIPTION
    Exit codes: 0 ok, 1 command not found, 2 non-zero exit, 4 timeout.
.EXAMPLE
    ./07_run_command.ps1 -TimeoutSeconds 5 -- ping -n 1 web01.example.invalid
#>
param(
    [int]$TimeoutSeconds = 10,

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Command
)

$ErrorActionPreference = 'Stop'

$EXIT_OK = 0
$EXIT_COMMAND_NOT_FOUND = 1
$EXIT_NONZERO = 2
$EXIT_TIMEOUT = 4

function Invoke-SafeCommand {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [string[]]$Arguments = @(),
        [Parameter(Mandatory = $true)][int]$TimeoutSeconds
    )

    if (-not (Get-Command -Name $Name -ErrorAction SilentlyContinue)) {
        [Console]::Error.WriteLine("command not found: $Name")
        return [pscustomobject]@{ Stdout = ''; Stderr = ''; ExitCode = $script:EXIT_COMMAND_NOT_FOUND }
    }

    $psi = [System.Diagnostics.ProcessStartInfo]::new()
    $psi.FileName = $Name
    foreach ($a in $Arguments) { $psi.ArgumentList.Add($a) }
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.UseShellExecute = $false

    $process = [System.Diagnostics.Process]::Start($psi)
    $stdoutTask = $process.StandardOutput.ReadToEndAsync()
    $stderrTask = $process.StandardError.ReadToEndAsync()

    if (-not $process.WaitForExit($TimeoutSeconds * 1000)) {
        try { $process.Kill() } catch { }
        [Console]::Error.WriteLine("timed out after ${TimeoutSeconds}s")
        return [pscustomobject]@{ Stdout = ''; Stderr = ''; ExitCode = $script:EXIT_TIMEOUT }
    }

    $stdout = $stdoutTask.GetAwaiter().GetResult()
    $stderr = $stderrTask.GetAwaiter().GetResult()

    if ($process.ExitCode -eq 0) {
        return [pscustomobject]@{ Stdout = $stdout; Stderr = $stderr; ExitCode = $script:EXIT_OK }
    }

    if ($stderr) { [Console]::Error.WriteLine($stderr.TrimEnd()) }
    return [pscustomobject]@{ Stdout = $stdout; Stderr = $stderr; ExitCode = $script:EXIT_NONZERO }
}

if (-not $Command -or $Command.Count -eq 0) {
    [Console]::Error.WriteLine('Usage: 07_run_command.ps1 [-TimeoutSeconds N] -- CMD [ARGS...]')
    exit $EXIT_COMMAND_NOT_FOUND
}

$commandArgs = $Command
if ($commandArgs[0] -eq '--') { $commandArgs = $commandArgs[1..($commandArgs.Count - 1)] }

$cmdName = $commandArgs[0]
$cmdArgs = @()
if ($commandArgs.Count -gt 1) { $cmdArgs = $commandArgs[1..($commandArgs.Count - 1)] }

$result = Invoke-SafeCommand -Name $cmdName -Arguments $cmdArgs -TimeoutSeconds $TimeoutSeconds
if ($result.Stdout) { Write-Output $result.Stdout }
exit $result.ExitCode
