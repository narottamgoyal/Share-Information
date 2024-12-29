# Define the task name and description
$TaskName = "DrinkWaterReminder"
$Description = "A task to remind you to drink water every hour."

# Define the action to show a message box
$Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument '-NoProfile -WindowStyle Hidden -Command "Add-Type -AssemblyName PresentationFramework; [System.Windows.MessageBox]::Show(\"Time to drink water! Stay hydrated!\", \"Drink Water Reminder\")"'

# Define the trigger to repeat every hour and expire in one year
$StartTime = Get-Date
$EndTime = $StartTime.AddYears(1)
$Trigger = New-ScheduledTaskTrigger -Once -At $StartTime -RepetitionInterval (New-TimeSpan -Hours 1) -RepetitionDuration ([TimeSpan]::FromDays(365))

# Register the task
Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Description $Description -User (whoami) -RunLevel Highest

Write-Output "Task '$TaskName' created successfully. It will expire on $EndTime."
