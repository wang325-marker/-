# SpringBoot 3.2.0 HelloWorld API

这是一个基于 SpringBoot 3.2.0 的 HelloWorld API 项目，包含 Spring Security 身份验证功能。

## 项目特性

- ✅ SpringBoot 3.2.0
- ✅ Spring Security 身份验证
- ✅ JWT Token 认证
- ✅ RESTful API 设计
- ✅ 用户名密码登录
- ✅ HelloWorld API (需要认证)

## 快速开始

### 环境要求

- Java 17+
- Maven 3.6+

### 运行项目

1. 编译项目
```bash
mvn clean compile
```

2. 运行项目
```bash
mvn spring-boot:run
```

3. 项目启动后访问: http://localhost:8080

## API 接口

### 1. 登录 API

**接口地址:** `POST /api/auth/login`

**请求体:**
```json
{
    "username": "test",
    "password": "123456"
}
```

**响应示例:**
```json
{
    "token": "eyJhbGciOiJIUzUxMiJ9...",
    "username": "test",
    "message": "登录成功",
    "expiresIn": 86400000
}
```

### 2. HelloWorld API

**接口地址:** `GET /api/hello`

**请求头:**
```
Authorization: Bearer <your-jwt-token>
```

**响应示例:**
```
Hello World! 欢迎您，test！
```

### 3. 获取当前用户信息

**接口地址:** `GET /api/user`

**请求头:**
```
Authorization: Bearer <your-jwt-token>
```

**响应示例:**
```
当前登录用户: test, 权限: [ROLE_USER]
```

### 4. 登录帮助

**接口地址:** `GET /api/auth/help`

获取登录相关的帮助信息和测试账号。

### 5. Token 验证

**接口地址:** `GET /api/auth/validate`

**请求头:**
```
Authorization: Bearer <your-jwt-token>
```

验证当前 Token 的有效性。

## 测试账号

| 用户名 | 密码 | 角色 |
|--------|------|------|
| test | 123456 | USER |
| admin | admin123 | ADMIN, USER |

## 使用示例

### 1. 登录获取 Token

```bash
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"123456"}'
```

### 2. 使用 Token 访问 HelloWorld API

```bash
curl -X GET http://localhost:8080/api/hello \
  -H "Authorization: Bearer <your-jwt-token>"
```

## 项目结构

```
src/main/java/com/example/
├── HelloWorldApplication.java          # 主应用类
├── config/
│   └── SecurityConfig.java            # Spring Security 配置
├── controller/
│   ├── AuthController.java            # 认证控制器
│   └── HelloController.java           # HelloWorld 控制器
├── dto/
│   ├── LoginRequest.java              # 登录请求 DTO
│   └── LoginResponse.java             # 登录响应 DTO
├── entity/
│   └── User.java                      # 用户实体
├── security/
│   └── JwtAuthenticationFilter.java   # JWT 认证过滤器
├── service/
│   └── UserService.java               # 用户服务
└── util/
    └── JwtUtil.java                   # JWT 工具类
```

## 技术栈

- **SpringBoot 3.2.0** - 主框架
- **Spring Security** - 安全框架
- **JWT** - Token 认证
- **Maven** - 依赖管理
- **Java 17** - 编程语言

## 开发说明

- JWT Token 有效期为 24 小时
- 密码使用 BCrypt 加密存储
- 支持 CORS 跨域请求
- 包含完整的错误处理和验证

## 许可证

MIT License