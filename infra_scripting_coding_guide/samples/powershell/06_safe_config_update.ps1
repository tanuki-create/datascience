#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Safely update a text configuration file.
.DESCRIPTION
    Takes a timestamped backup before writing, and replaces the target
    file atomically via a temporary file in the same directory plus
    Move-Item.

    WARNING: this script overwrites -Target in place (after backing it
    up). Do not point -Target at a production file without testing in a
    sandbox first.
#>
param(
    [Parameter(Mandatory = $true)]
    [string]$Target,

    [Parameter(Mandatory = $true)]
    [string]$ContentFile,

    [Parameter(Mandatory = $true)]
    [string]$BackupDir
)

$ErrorActionPreference = 'Stop'

function Backup-ConfigFile {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$BackupDir
    )
    New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
    $timestamp = [DateTimeOffset]::UtcNow.ToString('yyyyMMddTHHmmssZ')
    $name = Split-Path -Leaf $Path
    $dest = Join-Path $BackupDir "$name.$timestamp.bak"
    Copy-Item -LiteralPath $Path -Destination $dest
    return $dest
}

function Update-ConfigFile {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$NewContent,
        [Parameter(Mandatory = $true)][string]$BackupDir
    )

    $backup = $null
    if (Test-Path -LiteralPath $Path -PathType Leaf) {
        $backup = Backup-ConfigFile -Path $Path -BackupDir $BackupDir
    }

    $dir = Split-Path -Parent $Path
    if ([string]::IsNullOrEmpty($dir)) { $dir = '.' }
    $tmpPath = Join-Path $dir ("." + [System.IO.Path]::GetFileName($Path) + "." + [System.IO.Path]::GetRandomFileName())

    try {
        [System.IO.File]::WriteAllText($tmpPath, $NewContent, [System.Text.Encoding]::UTF8)
        Move-Item -LiteralPath $tmpPath -Destination $Path -Force
    }
    catch {
        Remove-Item -LiteralPath $tmpPath -ErrorAction SilentlyContinue
        throw
    }

    return $backup
}

if (-not (Test-Path -LiteralPath $ContentFile -PathType Leaf)) {
    [Console]::Error.WriteLine("content file not found: $ContentFile")
    exit 1
}

$newContent = Get-Content -LiteralPath $ContentFile -Raw -Encoding utf8
if ([string]::IsNullOrWhiteSpace($newContent)) {
    [Console]::Error.WriteLine('refusing to write empty content')
    exit 2
}

try {
    $backup = Update-ConfigFile -Path $Target -NewContent $newContent -BackupDir $BackupDir
}
catch {
    [Console]::Error.WriteLine($_.Exception.Message)
    exit 2
}

if ($backup) {
    [Console]::Error.WriteLine("backed up previous content to $backup")
}
else {
    [Console]::Error.WriteLine("no previous file; created $Target")
}

exit 0
