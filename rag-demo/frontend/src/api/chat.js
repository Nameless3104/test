// 使用相对路径，开发时由 Vite 代理，生产时由 Nginx 或同源访问
const API_BASE = '/api';

export async function sendQuestion(question) {
  const response = await fetch(`${API_BASE}/chat/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question })
  });
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  return response.json();
}

export async function getDocuments() {
  const response = await fetch(`${API_BASE}/documents/`);
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  return response.json();
}
