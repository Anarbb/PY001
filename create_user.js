db = db.getSiblingDB("usernames");
db.createUser({
  user: "fastapi_user",
  pwd: "your_password_here",
  roles: [{ role: "readWrite", db: "usernames" }]
});
