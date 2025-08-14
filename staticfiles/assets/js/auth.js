// --- MOCK AUTHENTICATION & BACKEND (No external dependencies) ---

// Define the mock users for the demo, including the static OTP for HR
const mockUsers = {
    employee: { email: 'employee@abcinc.com', password: 'password' },
    hr: { email: 'hr@abcinc.com', password: 'password', otp: '123456' } // Static OTP
};

/**
 * Simulates signing in a user with email and password.
 * This function ONLY checks email and password. OTP is handled separately in the UI flow.
 * @param {string} email
 * @param {string} password
 * @param {string} role - Either 'HR' or 'Employee'
 * @returns {Promise<object>} - A promise that resolves if login is successful, or rejects if not.
 */
async function mockSignIn(email, password, role) {
    const userType = role.toLowerCase();
    
    return new Promise((resolve, reject) => {
        // Simulate network delay
        setTimeout(() => {
            if (mockUsers[userType] && email === mockUsers[userType].email && password === mockUsers[userType].password) {
                console.log(`${role} credential check successful for ${email}`);
                resolve({
                    user: {
                        uid: `${userType}-12345`,
                        email: email
                    }
                });
            } else {
                console.error(`Credential check failed for ${email}`);
                reject(new Error('Invalid credentials. Please try again.'));
            }
        }, 500); // 0.5 second delay
    });
}

/**
 * Simulates signing out the current user.
 * @returns {Promise<void>}
 */
async function mockSignOut() {
    return new Promise((resolve) => {
        setTimeout(() => {
            console.log('User signed out.');
            resolve();
        }, 200);
    });
}

/**
 * This function is no longer active but is kept for future use.
 * @param {object} logData - The data to log.
 */
async function logToMongo(logData) {
    console.log("MongoDB logging is currently disabled.", logData);
}