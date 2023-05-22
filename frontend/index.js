const express = require("express");
const path = require("path");
const cookieParser = require("cookie-parser");
const dotenv = require("dotenv");
dotenv.config();

const registerRoute = require("./routes/auth/register");
const loginRoute = require("./routes/auth/login");
const userRoute = require("./routes/auth/user");
const logoutRoute = require("./routes/auth/logout");

const app = express();

app.use(express.json());
app.use(cookieParser());

app.use(registerRoute);
app.use(loginRoute);
app.use(userRoute);
app.use(logoutRoute);

app.use(express.static("app/build"));

app.get("*", (req, res) => {
  return res.sendFile(path.resolve(__dirname, "app", "build", "index.html"));
});

const PORT = process.env.PORT || 9000; //need to change port here

app.listen(PORT, () => console.log(`Server is listening on port ${PORT}`));
