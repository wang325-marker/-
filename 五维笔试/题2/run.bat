@echo off
echo ================================
echo SpringBoot HelloWorld API 启动脚本
echo ================================
echo.

echo 检查Java环境...
java -version
if %errorlevel% neq 0 (
    echo 错误: 未找到Java环境，请安装Java 17+
    pause
    exit /b 1
)

echo.
echo 检查Maven环境...
mvn -version
if %errorlevel% neq 0 (
    echo 错误: 未找到Maven环境，请安装Maven 3.6+
    echo 或者使用IDE（如IntelliJ IDEA或Eclipse）导入项目
    pause
    exit /b 1
)

echo.
echo 编译项目...
mvn clean compile
if %errorlevel% neq 0 (
    echo 编译失败，请检查代码
    pause
    exit /b 1
)

echo.
echo 启动应用...
mvn spring-boot:run

pause