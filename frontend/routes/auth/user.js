const express = require("express");
const cookie = require("cookie");
const fetch = (...args) =>
  import("node-fetch").then(({ default: fetch }) => fetch(...args));
const router = express.Router();

router.get("/api/user/:userId", async (req, res) => {
  const { access } = req.cookies;
  try {
    const apiRes = await fetch(
      `${process.env.BACKEND_API_URL}/api/user/${req.params.userId}`,
      {
        method: "GET",
        headers: {
          Accept: "application/json",
          Authorization: `Bearer ${access}`,
        },
      }
    );

    const data = await apiRes.json();
    return res.status(apiRes.status).json(data);
  } catch (err) {
    return res.status(500).json({
      error: "Something went wrong when trying to get user info",
    });
  }
});

module.exports = router;
