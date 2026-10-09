export interface UserPresence {
  userId: string;
  cursor: { x: number; y: number };
  role: "human" | "agent";
  lastActive: number;
}

export class PresenceManager {
  private presences = new Map<string, UserPresence>();

  public updatePresence(userId: string, role: "human" | "agent", x: number, y: number): UserPresence {
    const presence: UserPresence = {
      userId,
      cursor: { x, y },
      role,
      lastActive: Date.now(),
    };
    this.presences.set(userId, presence);
    return presence;
  }

  public removePresence(userId: string): void {
    this.presences.delete(userId);
  }

  public getAll(): UserPresence[] {
    return Array.from(this.presences.values());
  }
}
