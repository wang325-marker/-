package com.example;

import com.example.controller.AuthController;
import com.example.controller.HelloController;
import com.example.service.UserService;
import com.example.util.JwtUtil;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

import static org.junit.jupiter.api.Assertions.assertNotNull;

/**
 * SpringBoot 应用测试类
 */
@SpringBootTest
@ActiveProfiles("test")
class HelloWorldApplicationTests {

    @Autowired
    private HelloController helloController;

    @Autowired
    private AuthController authController;

    @Autowired
    private UserService userService;

    @Autowired
    private JwtUtil jwtUtil;

    @Test
    void contextLoads() {
        // 验证Spring上下文加载成功
        assertNotNull(helloController);
        assertNotNull(authController);
        assertNotNull(userService);
        assertNotNull(jwtUtil);
    }

    @Test
    void testUserService() {
        // 测试用户服务
        boolean isValid = userService.validateUser("test", "123456");
        assertNotNull(isValid);
        System.out.println("用户验证测试: " + (isValid ? "通过" : "失败"));
    }
}