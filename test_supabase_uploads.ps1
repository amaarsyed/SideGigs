# Supabase Upload Test Script
# Run this in PowerShell to test file uploads

$baseUrl = "http://localhost:8000/api"

Write-Host "🧪 Testing Supabase File Uploads" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

# 1. Login to get access token
Write-Host "`n1. Logging in..." -ForegroundColor Yellow
$loginData = @{
    username = "testuser"
    password = "testpass123"
} | ConvertTo-Json

try {
    $loginResponse = Invoke-RestMethod -Uri "$baseUrl/accounts/login/" -Method POST -Body $loginData -ContentType "application/json"
    $accessToken = $loginResponse.access
    Write-Host "✅ Login successful!" -ForegroundColor Green
} catch {
    Write-Host "❌ Login failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   Make sure you have a testuser account created" -ForegroundColor Yellow
    exit
}

$headers = @{
    "Authorization" = "Bearer $accessToken"
}

# 2. Test Resume Upload (if you have a test file)
Write-Host "`n2. Testing Resume Upload..." -ForegroundColor Yellow
Write-Host "   Note: This requires a test PDF file" -ForegroundColor Cyan

# Create a simple test file
$testContent = "This is a test resume content for testing uploads."
$testFile = "test_resume.txt"
$testContent | Out-File -FilePath $testFile -Encoding UTF8

try {
    $boundary = [System.Guid]::NewGuid().ToString()
    $LF = "`r`n"
    $bodyLines = (
        "--$boundary",
        "Content-Disposition: form-data; name=`"file`"; filename=`"$testFile`"",
        "Content-Type: text/plain",
        "",
        $testContent,
        "--$boundary--"
    ) -join $LF
    
    $uploadResponse = Invoke-RestMethod -Uri "$baseUrl/upload/resume/" -Method POST -Headers $headers -Body $bodyLines -ContentType "multipart/form-data; boundary=$boundary"
    Write-Host "✅ Resume upload successful!" -ForegroundColor Green
    Write-Host "   Download URL: $($uploadResponse.download_url)" -ForegroundColor Cyan
    Write-Host "   Resume ID: $($uploadResponse.id)" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Resume upload failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   Make sure Supabase is configured in .env" -ForegroundColor Yellow
}

# Clean up test file
if (Test-Path $testFile) {
    Remove-Item $testFile
}

# 3. Test ID Upload (if you have test images)
Write-Host "`n3. Testing ID Upload..." -ForegroundColor Yellow
Write-Host "   Note: This requires test image files" -ForegroundColor Cyan

# Create a simple test image file
$testImageContent = "fake image data"
$testImageFile = "test_id.jpg"
$testImageContent | Out-File -FilePath $testImageFile -Encoding UTF8

try {
    $boundary = [System.Guid]::NewGuid().ToString()
    $LF = "`r`n"
    $bodyLines = (
        "--$boundary",
        "Content-Disposition: form-data; name=`"id_image`"; filename=`"$testImageFile`"",
        "Content-Type: image/jpeg",
        "",
        $testImageContent,
        "--$boundary--"
    ) -join $LF
    
    $uploadResponse = Invoke-RestMethod -Uri "$baseUrl/upload/id/" -Method POST -Headers $headers -Body $bodyLines -ContentType "multipart/form-data; boundary=$boundary"
    Write-Host "✅ ID upload successful!" -ForegroundColor Green
    Write-Host "   Preview URL: $($uploadResponse.preview)" -ForegroundColor Cyan
    Write-Host "   Status: $($uploadResponse.status)" -ForegroundColor Cyan
} catch {
    Write-Host "❌ ID upload failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   Make sure Supabase is configured in .env" -ForegroundColor Yellow
}

# Clean up test file
if (Test-Path $testImageFile) {
    Remove-Item $testImageFile
}

Write-Host "`n🎉 Supabase Upload Testing Complete!" -ForegroundColor Green
Write-Host "`n📋 Available Upload Endpoints:" -ForegroundColor Yellow
Write-Host "   POST $baseUrl/upload/resume/ - Upload resume file" -ForegroundColor White
Write-Host "   POST $baseUrl/upload/id/ - Upload ID verification" -ForegroundColor White

Write-Host "`n🔧 Setup Required:" -ForegroundColor Cyan
Write-Host "   1. Copy env.example to .env" -ForegroundColor White
Write-Host "   2. Add your Supabase URL and service role key" -ForegroundColor White
Write-Host "   3. Create an 'uploads' bucket in Supabase" -ForegroundColor White
Write-Host "   4. Set bucket to private" -ForegroundColor White
