<#
services.ps1

Read-only inventory of running Windows services.
Designed for endpoint hygiene and security visibility.

Does NOT modify any service.
#>

$services = Get-CimInstance Win32_Service |
    Where-Object { $_.State -eq "Running" } |
    Select-Object Name, DisplayName, StartMode, State, StartName

$result = @()

foreach ($svc in $services) {
    $result += @{
        name         = $svc.Name
        display_name = $svc.DisplayName
        start_mode   = $svc.StartMode
        state        = $svc.State
        run_as       = $svc.StartName
    }
}

$risk = "low"
if ($result.Count -gt 60) {
    $risk = "medium"
}
if ($result.Count -gt 100) {
    $risk = "high"
}

$output = [ordered]@{
    check  = "services"
    status = "ok"
    data   = [ordered]@{
        risk_level       = $risk
        running_services = $result.Count
        services         = $result
    }
}

$output | ConvertTo-Json -Depth 5
