<#
startup_items.ps1

Read-only inventory of startup programs on Windows.
Collects registry-based and folder-based startup entries.

Does NOT disable or modify anything.
#>

$startupItems = @()

# Registry paths
$registryPaths = @(
    "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run",
    "HKCU:\Software\Microsoft\Windows\CurrentVersion\RunOnce",
    "HKLM:\Software\Microsoft\Windows\CurrentVersion\Run",
    "HKLM:\Software\Microsoft\Windows\CurrentVersion\RunOnce"
)

foreach ($path in $registryPaths) {
    if (Test-Path $path) {
        Get-ItemProperty $path | Get-Member -MemberType NoteProperty | ForEach-Object {
            $startupItems += @{
                source  = "registry"
                location = $path
                name    = $_.Name
                command = (Get-ItemProperty $path).$($_.Name)
            }
        }
    }
}

# Startup folders
$startupFolders = @(
    "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup",
    "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup"
)

foreach ($folder in $startupFolders) {
    if (Test-Path $folder) {
        Get-ChildItem $folder | ForEach-Object {
            $startupItems += @{
                source  = "startup_folder"
                location = $folder
                name    = $_.Name
                command = $_.FullName
            }
        }
    }
}

$risk = "low"
if ($startupItems.Count -gt 10) {
    $risk = "medium"
}
if ($startupItems.Count -gt 20) {
    $risk = "high"
}

$output = @{
    check  = "startup_items"
    status = "ok"
    data   = @{
        count      = $startupItems.Count
        items      = $startupItems
        risk_level = $risk
    }
}

$output | ConvertTo-Json -Depth 5
