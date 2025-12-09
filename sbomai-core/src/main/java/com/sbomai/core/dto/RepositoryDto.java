package com.sbomai.core.dto;

public class RepositoryDto {
    
    private String url;
    private String type; // github, gitlab, bitbucket
    private String branch;
    
    // Constructors
    public RepositoryDto() {}
    
    public RepositoryDto(String url, String type, String branch) {
        this.url = url;
        this.type = type;
        this.branch = branch;
    }
    
    // Getters and Setters
    public String getUrl() { return url; }
    public void setUrl(String url) { this.url = url; }
    
    public String getType() { return type; }
    public void setType(String type) { this.type = type; }
    
    public String getBranch() { return branch; }
    public void setBranch(String branch) { this.branch = branch; }
} 