db = db.getSiblingDB('admin');

db.auth("admin", "admin_password");

db = db.getSiblingDB('usernames');

db.createUser({
  user: "anas",
  pwd: "asecretpassword",
  roles: [{ role: "readWrite", db: "usernames" }]
});

db.createCollection('usernames');
