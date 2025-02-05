# ====================== 热点应用 ======================
# 1. vscode
set-alias code "C:\tieshan\toolkit\dev\vscode\bin\code"
# 2. msedge
set-alias msedge "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


# ====================== 快捷命令 ======================
# 1. rm
function _rm { Remove-Item -Force -Recurse $args }
Remove-Item alias:rm
set-alias rm _rm

# 2. ls
function _ls { Get-ChildItem -Force $args }
Remove-Item alias:ls
set-alias ls _ls


# ====================== 函数重载 ======================
# 1. prompt
function prompt {
    # return "PS $($executionContext.SessionState.Path.CurrentLocation)$('>' * ($nestedPromptLevel + 1)) ";
    # .Link
    # https://go.microsoft.com/fwlink/?LinkID=225750
    # .ExternalHelp System.Management.Automation.dll-help.xml

    $datetime  = Get-Date -Format "yyyy-MM-dd HH:mm:ss";
    $battery   = "bat:$((Get-WmiObject -Class WIN32_Battery).EstimatedChargeRemaining)%";
    # $cpu       = "cpu:$(Get-WmiObject -Class Win32_Processor | Select LoadPercentage)%";
    # $os        = Get-WmiObject -Class WIN32_OperatingSystem;
    # $mem_total = $os.TotalVisibleMemorySize/1024/1024;
    # $mem_usage = $os.TotalVisibleMemorySize/1024/1024 - $os.FreePhysicalMemory/1024/1024;
    # $mem       = "memory:$mem_usage/$mem_total";
    $location  = Split-Path $(pwd) -Leaf;
    Write-Host -ForegroundColor blue -NoNewline "[$datetime] [$battery] ";
    Write-Host -ForegroundColor yellow -NoNewline "$location>";
    return " ";
}
