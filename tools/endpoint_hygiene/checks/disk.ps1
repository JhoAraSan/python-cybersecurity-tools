<#
disk_type.ps1

Read-only check to detect disk type (SSD / HDD) and basic disk metadata.
Designed for endpoint hygiene auditing.

Does NOT modify disk settings.
#>

$disks = Get-PhysicalDisk | Select-Object `
    FriendlyName,
    MediaType,
    Size,
    HealthStatus,
    OperationalStatus

$result = @()

foreach ($disk in $disks) {
    $result += @{
        name               = $disk.FriendlyName
        media_type         = $disk.MediaType.ToString()
        size_gb            = [math]::Round($disk.Size / 1GB, 2)
        health_status      = $disk.HealthStatus
        operational_status = $disk.OperationalStatus
    }
}

$overallRisk = "low"

if ($result.media_type -contains "HDD") {
    $overallRisk = "medium"
}

$output =[ordered]@{
    check  = "disk_type"
    status = "ok"
    data   = [ordered]@{
        risk_level = $overallRisk
        disks      = $result
    }
}

$output | ConvertTo-Json -Depth 4
