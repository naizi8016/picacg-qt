@echo off
REM 优化的Nuitka构建命令，适用于8核心CPU
REM 主要优化点：
REM 1. 设置合理的并行任务数（4个，为8核心的一半，避免系统资源耗尽）
REM 2. 移除--clang参数，使用更稳定的MSVC编译器
REM 3. 移除--onefile-no-compression，允许压缩以提高构建效率
REM 4. 添加--verbose参数以便更好地诊断问题
REM 5. 添加--lto=no禁用链接时优化，减少最后阶段卡住风险

cd /d "%~dp0\src"

python -m nuitka `
  --onefile `
  --output-dir=dist `
  --output-filename=PicACG `
  --windows-console-mode=disable `
  --msvc=latest `
  --assume-yes-for-downloads `
  --windows-icon-from-ico=icon.ico `
  --plugin-enable=pyside6,upx --upx-binary="D:\upx-5.0.1-win64" `
  --jobs=4 `
  --verbose `
  --lto=no `
  start.py

REM 如果需要恢复使用Clang，可以使用以下备用命令（取消注释）
REM python -m nuitka `
REM   --onefile `
REM   --output-dir=dist `
REM   --output-filename=PicACG `
REM   --windows-console-mode=disable `
REM   --msvc=latest `
REM   --clang `
REM   --assume-yes-for-downloads `
REM   --windows-icon-from-ico=icon.ico `
REM   --plugin-enable=pyside6,upx --upx-binary="D:\upx-5.0.1-win64" `
REM   --jobs=2 `
REM   --verbose `
REM   start.py

pause