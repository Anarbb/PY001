// Authenticate as root admin
db = db.getSiblingDB('admin');
db.auth("admin", "admin_password");

// Switch to the desired database (usernames in your case)
db = db.getSiblingDB('usernames');

// Create a user with readWrite access for the FastAPI app
db.createUser({
  user: "anas",
  pwd: "asecretpassword",
  roles: [{ role: "readWrite", db: "usernames" }]
});

// Create a collection in the database
db.createCollection('usernames');
