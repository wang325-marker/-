package com.example.controller;

import com.example.dto.LoginRequest;
import com.example.dto.LoginResponse;
import com.example.entity.User;
import com.example.service.UserService;
import com.example.util.JwtUtil;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

/**
 * 认证控制器
 * 处理用户登录等认证相关操作
 */
@RestController
@RequestMapping("/api/auth")
public class AuthController {

    @Autowired
    private UserService userService;

    @Autowired
    private JwtUtil jwtUtil;

    /**
     * 用户登录API
     * 
     * @param loginRequest 登录请求（用户名和密码）
     * @return 登录响应（包含JWT Token）
     */
    @PostMapping("/login")
    public ResponseEntity<?> login(@Valid @RequestBody LoginRequest loginRequest) {
        try {
            // 验证用户名和密码
            boolean isValid = userService.validateUser(
                loginRequest.getUsername(), 
                loginRequest.getPassword()
            );

            if (!isValid) {
                Map<String, String> error = new HashMap<>();
                error.put("error", "用户名或密码错误");
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(error);
            }

            // 加载用户详情
            UserDetails userDetails = userService.loadUserByUsername(loginRequest.getUsername());
            
            // 生成JWT Token
            String token = jwtUtil.generateToken(userDetails);
            
            // 创建登录响应
            LoginResponse response = new LoginResponse(
                token,
                userDetails.getUsername(),
                "登录成功",
                jwtUtil.getExpirationTime()
            );

            return ResponseEntity.ok(response);

        } catch (Exception e) {
            Map<String, String> error = new HashMap<>();
            error.put("error", "登录失败: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
        }
    }

    /**
     * 获取登录帮助信息
     */
    @GetMapping("/help")
    public ResponseEntity<Map<String, Object>> getLoginHelp() {
        Map<String, Object> help = new HashMap<>();
        help.put("message", "HelloWorld API 登录帮助");
        help.put("loginUrl", "/api/auth/login");
        help.put("method", "POST");
        help.put("testUser", Map.of(
            "username", "test",
            "password", "123456"
        ));
        help.put("adminUser", Map.of(
            "username", "admin", 
            "password", "admin123"
        ));
        help.put("example", Map.of(
            "request", Map.of(
                "username", "test",
                "password", "123456"
            ),
            "response", Map.of(
                "token", "eyJhbGciOiJIUzUxMiJ9...",
                "username", "test",
                "message", "登录成功",
                "expiresIn", 86400000
            )
        ));
        
        return ResponseEntity.ok(help);
    }

    /**
     * 验证Token有效性
     */
    @GetMapping("/validate")
    public ResponseEntity<Map<String, Object>> validateToken(@RequestHeader("Authorization") String authHeader) {
        try {
            if (authHeader != null && authHeader.startsWith("Bearer ")) {
                String token = authHeader.substring(7);
                String username = jwtUtil.extractUsername(token);
                UserDetails userDetails = userService.loadUserByUsername(username);
                
                boolean isValid = jwtUtil.validateToken(token, userDetails);
                
                Map<String, Object> result = new HashMap<>();
                result.put("valid", isValid);
                result.put("username", username);
                result.put("expiration", jwtUtil.extractExpiration(token));
                
                return ResponseEntity.ok(result);
            } else {
                Map<String, Object> error = new HashMap<>();
                error.put("error", "无效的Authorization头");
                return ResponseEntity.badRequest().body(error);
            }
        } catch (Exception e) {
            Map<String, Object> error = new HashMap<>();
            error.put("error", "Token验证失败: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(error);
        }
    }
}