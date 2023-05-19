const express = require("express");
const path = require("path");

const app = express();

app.use(express.static("app/build"));

app.get("*", (req, res) => {
  return res.sendFile(path.resolve(__dirname, "app", "build", "index.html"));
});

const PORT = process.env.PORT || 9000; //need to change port here

app.listen(PORT, () => console.log(`Server is listening on port ${PORT}`));
