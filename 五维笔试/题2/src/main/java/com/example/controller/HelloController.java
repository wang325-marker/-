package com.example.controller;

import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * HelloWorld API 控制器
 */
@RestController
@RequestMapping("/api")
public class HelloController {

    /**
     * HelloWorld API
     * 需要身份验证才能访问
     * 
     * @return Hello World 字符串
     */
    @GetMapping("/hello")
    public String hello() {
        // 获取当前认证用户信息
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        String username = authentication.getName();
        
        return "Hello World! 欢迎您，" + username + "！";
    }

    /**
     * 获取当前用户信息
     * 
     * @return 用户信息
     */
    @GetMapping("/user")
    public String getCurrentUser() {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        return "当前登录用户: " + authentication.getName() + 
               ", 权限: " + authentication.getAuthorities().toString();
    }
}