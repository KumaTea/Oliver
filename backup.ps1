$today = Get-Date -Format "yyyyMMdd"
Compress-Archive -Path "C:\Users\Administrator\Documents\vote", "C:\Users\Administrator\Documents\Oliver\tum" -DestinationPath "D:\FS\Backup\$today.zip"