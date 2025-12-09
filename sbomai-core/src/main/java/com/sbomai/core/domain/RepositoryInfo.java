package com.sbomai.core.domain;

import jakarta.persistence.Embeddable;
import jakarta.persistence.Column;

@Embeddable
public class RepositoryInfo {
    
    @Column(name = "repo_url")
    private String url;
    
    @Column(name = "repo_type")
    private String type; // github, gitlab, bitbucket
    
    @Column(name = "repo_branch")
    private String branch;
    
    // Constructors
    public RepositoryInfo() {}
    
    public RepositoryInfo(String url, String type, String branch) {
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