const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

const server = http.createServer(app);

const io = new Server(server, {
    cors: {
        origin: "*",
        methods: ["GET", "POST"]
    }
});

app.post('/api/send-odds', (req, res) => {
    const incomingOdds = req.body.odds;
    console.log(`📡 Bot Received Odds: ${incomingOdds}x`);

    if (incomingOdds) {
        io.emit('new_live_odds', { odds: incomingOdds });
        return res.status(200).json({ success: true, message: "Odds broadcasted!" });
    }
    return res.status(400).json({ success: false, message: "No odds found." });
});

app.get('/', (req, res) => {
    res.send("Aviator Live Engine Cloud Server is Running!");
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log(`🚀 Server is listening on port ${PORT}`);
});
