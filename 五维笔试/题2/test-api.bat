@echo off
echo ================================
echo HelloWorld API 测试脚本
echo ================================
echo.

set SERVER_URL=http://localhost:8080

echo 1. 测试登录帮助接口...
curl -X GET %SERVER_URL%/api/auth/help
echo.
echo.

echo 2. 测试用户登录...
curl -X POST %SERVER_URL%/api/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"test\",\"password\":\"123456\"}"
echo.
echo.

echo 请复制上面返回的token，然后手动测试HelloWorld API:
echo curl -X GET %SERVER_URL%/api/hello -H "Authorization: Bearer YOUR_TOKEN"
echo.

pause