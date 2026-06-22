@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: 【安全保险 1】获取当前脚本所在的文件夹路径
set "CURRENT_DIR=%~dp0"

:: 【安全保险 2】检查路径是否获取成功，如果失败直接退出，防止空路径导致误操作
if "%CURRENT_DIR%"=="" (
    echo [错误] 无法获取当前目录路径，脚本安全终止！
    pause
    exit /b 1
)

:: 【安全保险 3】强制将生成的 TXT 放在“桌面”，绝对不污染模型文件夹
set "DESKTOP_PATH=%USERPROFILE%\Desktop"
set "OUTPUT_FILE=%DESKTOP_PATH%\triggers_template.txt"

:: 在桌面创建或覆盖 TXT 文件（只针对桌面的这一个文件，绝对安全）
echo. > "%OUTPUT_FILE%"

:: 遍历当前模型目录下的 safetensors 和 ckpt 文件
for %%F in ("%CURRENT_DIR%*.safetensors" "%CURRENT_DIR%*.ckpt") do (
    set "FILENAME=%%~nxF"
    :: 以追加模式写入桌面 TXT 文件
    echo !FILENAME!="" >> "%OUTPUT_FILE%"
)

echo ========================================
echo  模板生成完毕！
echo  文件已安全保存在您的【桌面】：
echo  %OUTPUT_FILE%
echo ========================================
pause