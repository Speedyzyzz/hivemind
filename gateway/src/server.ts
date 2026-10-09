import { WebSocketServer, WebSocket } from "ws";
import { CollaborativeRoom } from "./rooms.js";

const PORT = 4000;
const wss = new WebSocketServer({ port: PORT });
const rooms = new Map<string, CollaborativeRoom>();

function getOrCreateRoom(roomId: string): CollaborativeRoom {
  let room = rooms.get(roomId);
  if (!room) {
    room = new CollaborativeRoom(roomId);
    rooms.set(roomId, room);
  }
  return room;
}

wss.on("connection", (ws: WebSocket) => {
  let currentRoomId: string | null = null;
  let currentUserId: string | null = null;

  ws.on("message", (raw: string) => {
    try {
      const data = JSON.parse(raw.toString());
      if (data.type === "join") {
        currentRoomId = data.roomId;
        currentUserId = data.userId;
        const room = getOrCreateRoom(currentRoomId!);
        room.presence.updatePresence(currentUserId!, data.role || "human", 0, 0);

        ws.send(JSON.stringify({
          type: "sync_state",
          intentDoc: room.intentDoc,
          presence: room.presence.getAll(),
        }));
      } else if (data.type === "cursor") {
        if (currentRoomId && currentUserId) {
          const room = getOrCreateRoom(currentRoomId);
          room.presence.updatePresence(currentUserId, data.role || "human", data.x, data.y);
          // Broadcast presence
          const payload = JSON.stringify({ type: "presence_update", presence: room.presence.getAll() });
          wss.clients.forEach((client) => {
            if (client.readyState === WebSocket.OPEN) client.send(payload);
          });
        }
      }
    } catch {
      // Ignore malformed payloads
    }
  });

  ws.on("close", () => {
    if (currentRoomId && currentUserId) {
      const room = rooms.get(currentRoomId);
      if (room) {
        room.presence.removePresence(currentUserId);
      }
    }
  });
});

console.log(`HiveMind Collaborative WebSocket Gateway running on ws://localhost:${PORT}`);
