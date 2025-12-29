// auth.js - Authentication JavaScript

const API_BASE_URL = 'http://127.0.0.1:5000';  // Change from localhost

// ==================== SIGNUP ====================
async function handleSignup(event) {
    event.preventDefault();
    
    const username = document.getElementById('signup-username').value;
    const password = document.getElementById('signup-password').value;
    const confirmPassword = document.getElementById('signup-confirm-password').value;
    
    if (password !== confirmPassword) {
        alert('Passwords do not match!');
        return;
    }
    
    console.log('Attempting signup...'); // Debug log
    
    try {
        const response = await fetch(`${API_BASE_URL}/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({
                username: username,
                password: password
            })
        });
        
        const data = await response.json();
        console.log('Response:', data); // Debug log
        
        if (response.ok) {
            alert('Account created successfully!');
            window.location.href = 'login.html';
        } else {
            alert('Signup failed: ' + (data.error || 'Unknown error'));
        }
        
    } catch (error) {
        console.error('Error:', error);
        alert('Connection error! Make sure backend is running on port 5000');
    }
}

// ==================== LOGIN ====================
async function handleLogin(event) {
    event.preventDefault();
    
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    
    console.log('Attempting login...'); // Debug log
    
    try {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({
                username: username,
                password: password
            })
        });
        
        const data = await response.json();
        console.log('Response:', data); // Debug log
        
        if (response.ok) {
            localStorage.setItem('username', username);
            localStorage.setItem('isLoggedIn', 'true');
            alert('Login successful!');
            window.location.href = 'dashboard.html';
        } else {
            alert('Login failed: ' + (data.error || 'Invalid credentials'));
        }
        
    } catch (error) {
        console.error('Error:', error);
        alert('Connection error! Make sure backend is running on port 5000');
    }
}

// ==================== LOGOUT ====================
async function handleLogout() {
    try {
        await fetch(`${API_BASE_URL}/logout`, {
            method: 'POST',
            credentials: 'include'
        });
        
        localStorage.clear();
        alert('Logged out successfully!');
        window.location.href = 'index.html';
        
    } catch (error) {
        console.error('Error:', error);
        localStorage.clear();
        window.location.href = 'index.html';
    }
}

// ==================== CHECK AUTH ====================
function checkAuth() {
    const isLoggedIn = localStorage.getItem('isLoggedIn');
    if (!isLoggedIn) {
        alert('Please log in first');
        window.location.href = 'login.html';
    }
}

// ==================== TOGGLE PASSWORD ====================
function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    input.type = input.type === 'password' ? 'text' : 'password';
}

// ==================== DISPLAY USERNAME ====================
function displayUsername() {
    const username = localStorage.getItem('username');
    if (username) {
        const welcomeElement = document.querySelector('.user-welcome h1');
        if (welcomeElement) {
            welcomeElement.textContent = `Welcome back, ${username}!`;
        }
    }
}
