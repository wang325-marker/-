package com.example.service;

import com.example.entity.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * 用户服务类
 * 实现 Spring Security 的 UserDetailsService 接口
 */
@Service
public class UserService implements UserDetailsService {

    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();
    
    // 模拟用户数据库，实际项目中应该使用真实的数据库
    private final Map<String, User> users = new HashMap<>();

    public UserService() {
        // 初始化测试用户: test / 123456
        User testUser = new User(
            "test", 
            passwordEncoder.encode("123456"), 
            List.of("USER")
        );
        users.put("test", testUser);
        
        // 可以添加更多测试用户
        User adminUser = new User(
            "admin", 
            passwordEncoder.encode("admin123"), 
            List.of("ADMIN", "USER")
        );
        users.put("admin", adminUser);
    }

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        User user = users.get(username);
        if (user == null) {
            throw new UsernameNotFoundException("用户不存在: " + username);
        }
        return user;
    }

    /**
     * 验证用户登录
     */
    public boolean validateUser(String username, String password) {
        try {
            User user = (User) loadUserByUsername(username);
            return passwordEncoder.matches(password, user.getPassword());
        } catch (UsernameNotFoundException e) {
            return false;
        }
    }

    /**
     * 根据用户名获取用户
     */
    public User getUserByUsername(String username) {
        return users.get(username);
    }
}