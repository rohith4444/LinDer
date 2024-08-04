function Show-ProjectStructure {
    param (
        [string]$path = ".",
        [string]$indent = ""
    )

    $exclude = @("venv", "__pycache__")
    $items = Get-ChildItem -Path $path -Exclude $exclude

    foreach ($item in $items) {
        Write-Host "$indent+---$($item.Name)"
        if ($item.PSIsContainer) {
            Show-ProjectStructure -path $item.FullName -indent "$indent|   "
        }
    }
}

Show-ProjectStructure