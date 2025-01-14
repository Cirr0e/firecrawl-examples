use std::error::Error;
use serde::{Serialize, Deserialize};

/// Core data model for tasks in FlowSync
#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Task {
    pub id: String,
    pub title: String,
    pub description: Option<String>,
    pub status: TaskStatus,
    pub priority: TaskPriority,
    pub ai_insights: Option<AIInsights>,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub enum TaskStatus {
    Todo,
    InProgress,
    Done,
    Blocked,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub enum TaskPriority {
    Low,
    Medium,
    High,
    Critical,
}

/// AI-generated insights for tasks
#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct AIInsights {
    pub complexity: f32,
    pub recommended_subtasks: Vec<String>,
    pub potential_blockers: Vec<String>,
}

/// Encryption service for local data protection
pub struct EncryptionService {
    // Placeholder for encryption logic
}

impl EncryptionService {
    pub fn encrypt(data: &str) -> Result<String, Box<dyn Error>> {
        // TODO: Implement AES-256 encryption
        Ok(data.to_string())
    }

    pub fn decrypt(encrypted_data: &str) -> Result<String, Box<dyn Error>> {
        // TODO: Implement AES-256 decryption
        Ok(encrypted_data.to_string())
    }
}