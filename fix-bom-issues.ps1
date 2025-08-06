# Fix BOM Encoding Issues in Java Files
# This script removes UTF-8 BOM characters from Java source files

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "FIXING BOM ENCODING ISSUES IN JAVA FILES" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$javaFiles = Get-ChildItem -Path "src" -Filter "*.java" -Recurse
$fixedCount = 0

foreach ($file in $javaFiles) {
    Write-Host "Processing: $($file.FullName)" -ForegroundColor Yellow
    
    # Read file content as bytes to detect BOM
    $content = [System.IO.File]::ReadAllBytes($file.FullName)
    
    # Check if file starts with UTF-8 BOM (EF BB BF)
    if ($content.Length -ge 3 -and $content[0] -eq 0xEF -and $content[1] -eq 0xBB -and $content[2] -eq 0xBF) {
        Write-Host "  Found BOM - Removing..." -ForegroundColor Red
        
        # Remove BOM and write back
        $newContent = $content[3..($content.Length-1)]
        [System.IO.File]::WriteAllBytes($file.FullName, $newContent)
        
        $fixedCount++
        Write-Host "  Fixed!" -ForegroundColor Green
    } else {
        Write-Host "  No BOM found - OK" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "BOM FIX COMPLETED!" -ForegroundColor Cyan
Write-Host "Files fixed: $fixedCount" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Test compilation
Write-Host "Testing compilation..." -ForegroundColor Yellow
mvn clean compile

Write-Host ""
Write-Host "Done!" -ForegroundColor Green 