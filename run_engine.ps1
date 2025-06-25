# PowerShell script to run the engine
Write-Host "?? Starting AI Social Media Content Engine..." -ForegroundColor Green
Write-Host ""
Write-Host "Make sure you have:" -ForegroundColor Yellow
Write-Host "  1. Added OPENAI_API_KEY to .env file" -ForegroundColor White
Write-Host "  2. Installed requirements: pip install -r requirements.txt" -ForegroundColor White
Write-Host ""
Read-Host "Press Enter to continue..."
python free_posting_main.py
Read-Host "Press Enter to exit..."
