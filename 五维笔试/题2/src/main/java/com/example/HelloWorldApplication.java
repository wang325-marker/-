package com.example;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * SpringBoot 3.2.0 HelloWorld API 主应用类
 * 
 * @author CodeBuddy
 * @version 1.0.0
 */
@SpringBootApplication
public class HelloWorldApplication {

    public static void main(String[] args) {
        SpringApplication.run(HelloWorldApplication.class, args);
        System.out.println("=================================");
        System.out.println("HelloWorld API 启动成功！");
        System.out.println("访问地址: http://localhost:8080");
        System.out.println("HelloWorld API: GET /api/hello");
        System.out.println("登录 API: POST /api/auth/login");
        System.out.println("测试用户: test / 123456");
        System.out.println("=================================");
    }
}