# 13_classify_disk.ps1 のPesterテスト。
#
# 実行方法:
#   Invoke-Pester ./tests/13_classify_disk.Tests.ps1 -Output Detailed

BeforeAll {
    . "$PSScriptRoot/../samples/powershell/13_classify_disk.ps1"
}

Describe 'Get-DiskStatus' {
    It 'returns ok for usage below warn threshold' {
        Get-DiskStatus -UsedPercent 50 -WarnPercent 80 -CritPercent 90 | Should -Be 'ok'
    }

    It 'returns warning exactly at warn threshold' {
        Get-DiskStatus -UsedPercent 80 -WarnPercent 80 -CritPercent 90 | Should -Be 'warning'
    }

    It 'returns warning below crit threshold' {
        Get-DiskStatus -UsedPercent 89 -WarnPercent 80 -CritPercent 90 | Should -Be 'warning'
    }

    It 'returns critical exactly at crit threshold' {
        Get-DiskStatus -UsedPercent 90 -WarnPercent 80 -CritPercent 90 | Should -Be 'critical'
    }

    It 'returns critical at the upper bound of 100' {
        Get-DiskStatus -UsedPercent 100 -WarnPercent 80 -CritPercent 90 | Should -Be 'critical'
    }

    It 'returns ok at the lower bound of 0' {
        Get-DiskStatus -UsedPercent 0 -WarnPercent 80 -CritPercent 90 | Should -Be 'ok'
    }

    It 'throws when warn threshold exceeds crit threshold' {
        { Get-DiskStatus -UsedPercent 85 -WarnPercent 90 -CritPercent 80 } | Should -Throw
    }

    It 'throws when used percent is negative' {
        { Get-DiskStatus -UsedPercent -1 -WarnPercent 80 -CritPercent 90 } | Should -Throw
    }

    It 'throws when used percent exceeds 100' {
        { Get-DiskStatus -UsedPercent 150 -WarnPercent 80 -CritPercent 90 } | Should -Throw
    }
}

Describe 'Invoke-DiskClassification' {
    It 'reports the worst status across multiple mount points' {
        $usages = @(
            [pscustomobject]@{ MountPoint = 'C:'; UsedPercent = 50 }
            [pscustomobject]@{ MountPoint = 'D:'; UsedPercent = 95 }
        )
        $report = Invoke-DiskClassification -Usages $usages -WarnPercent 80 -CritPercent 90
        $report.Worst | Should -Be 'critical'
        ($report.Results | Where-Object { $_.MountPoint -eq 'D:' }).Status | Should -Be 'critical'
    }

    It 'returns ok as the worst status when everything is fine' {
        $usages = @(
            [pscustomobject]@{ MountPoint = 'C:'; UsedPercent = 10 }
            [pscustomobject]@{ MountPoint = 'D:'; UsedPercent = 20 }
        )
        $report = Invoke-DiskClassification -Usages $usages -WarnPercent 80 -CritPercent 90
        $report.Worst | Should -Be 'ok'
    }
}

Describe 'Invoke-Main' {
    It 'returns exit code 3 when a mocked disk is critical' {
        Mock Get-LocalDiskUsage {
            @([pscustomobject]@{ MountPoint = 'C:'; UsedPercent = 95 })
        }
        Invoke-Main -WarnPercent 80 -CritPercent 90 | Should -Be 3
    }

    It 'returns exit code 0 when all mocked disks are ok' {
        Mock Get-LocalDiskUsage {
            @([pscustomobject]@{ MountPoint = 'C:'; UsedPercent = 10 })
        }
        Invoke-Main -WarnPercent 80 -CritPercent 90 | Should -Be 0
    }

    It 'returns exit code 1 when thresholds are invalid' {
        Mock Get-LocalDiskUsage {
            @([pscustomobject]@{ MountPoint = 'C:'; UsedPercent = 50 })
        }
        Invoke-Main -WarnPercent 90 -CritPercent 80 | Should -Be 1
    }
}
