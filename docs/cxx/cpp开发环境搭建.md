# cpp开发环境搭建


## 参考


## 1 vscode
1. [官网](https://code.visualstudio.com/)下载vscode安装包
2. 根据指引安装vscode
3. 安装插件
   <!-- - ms-vscode.cpptools
   - ms-vscode.cpptools-extension-pack -->
   - twxs.cmake
   - ms-vscode.cmake-tools
   - llvm-vs-code-extensions.vscode-clangd
4. 配置(见附录)
   - c_cpp_properties.json
   - launch.json
   - tasks.json


## 2 mingw64
1. [官网](https://www.mingw-w64.org/downloads/)下载对应版本的安装包
   windows系统可以选择WinLibs.com, 下载解压即可
2. 将bin目录添加到环境变量
3. 测试是否安装成功: `g++ --version`


## 3 cmake
1. [官网](https://cmake.org/download/)下载对应版本的安装包
2. 将bin目录添加到环境变量
3. 测试是否安装成功: `cmake --version`


## Appendix
### c_cpp_properties.json
```json
{
    "version": 4,
    "configurations": [
        {
            "name": "manjaro",
            "includePath": [
                "${workspaceFolder}/include/"
            ],
            "defines": [
                "_DEBUG",
                "UNICODE",
                "_UNICODE"
            ],
            "compilerPath": "C:\\tieshan_wu\\devenv\\mingw64\\13.2.0\\bin\\g++.exe",
            "cStandard": "c17",
            "cppStandard": "c++17",
            "intelliSenseMode": "windows-gcc-x64",
            "browse": {
                "path": [
                    "${workspaceFolder}"
                ],
                "limitSymbolsToIncludedHeaders": true,
                "databaseFilename": ""
            },
            "configurationProvider": "ms-vscode.cmake-tools"
        }
    ]
}
```


### launch.json
```json
{
    // 使用 IntelliSense 了解相关属性。 
    // 悬停以查看现有属性的描述。
    // 欲了解更多信息，请访问: https://go.microsoft.com/fwlink/?linkid=830387
    
    
    "version": "0.2.0",
    "configurations": [
        {
            "name": "cppdbg",
            "type": "cppdbg",
            "request": "launch",
            "program": "${command:cmake.launchTargetPath}",
            "args": [],
            "stopAtEntry": false,
            "cwd": "${command:cmake.launchTargetDirectory}",
            "environment": [],
            "externalConsole": false,
            "MIMode": "gdb",
            "miDebuggerPath": "C:\\tieshan_wu\\devenv\\mingw64\\13.2.0\\bin\\gdb.exe",
            "preLaunchTask": "cmake: cleanRebuild",//对应于tasks.json中的label
            "setupCommands": [
                {
                    "description": "为 gdb 启用整齐打印",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures": true
                },
                {
                    "description": "将反汇编风格设置为 Intel",
                    "text": "-gdb-set disassembly-flavor intel",
                    "ignoreFailures": true
                }
            ]
        }
    ]
}
```


### tasks.json
```json
{
    "version": "2.0.0",
    "options": {},
    "tasks": [
        {
            "type": "cmake",
            "label": "cmake: cleanRebuild",
            "command": "cleanRebuild",
            "targets": [],
            "group": {
                "kind": "build",
                "isDefault": true
            }
        }
    ]
}
```
