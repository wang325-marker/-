package com.example.dto;

/**
 * 登录响应DTO
 */
public class LoginResponse {
    
    private String token;
    private String username;
    private String message;
    private long expiresIn;

    public LoginResponse() {}

    public LoginResponse(String token, String username, String message, long expiresIn) {
        this.token = token;
        this.username = username;
        this.message = message;
        this.expiresIn = expiresIn;
    }

    public String getToken() {
        return token;
    }

    public void setToken(String token) {
        this.token = token;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public long getExpiresIn() {
        return expiresIn;
    }

    public void setExpiresIn(long expiresIn) {
        this.expiresIn = expiresIn;
    }
}