import { PresenceManager } from "./presence.js";

export interface CollaborativeIntentDoc {
  goal: string;
  tasks: Array<{ id: string; title: string; assignedTo: string; status: string }>;
  version: number;
}

export class CollaborativeRoom {
  public presence = new PresenceManager();
  public intentDoc: CollaborativeIntentDoc;

  constructor(public roomId: string) {
    this.intentDoc = {
      goal: "Shared Agent Objective",
      tasks: [],
      version: 1,
    };
  }

  public applyIntentMutation(mutation: Partial<CollaborativeIntentDoc>): CollaborativeIntentDoc {
    if (mutation.goal) this.intentDoc.goal = mutation.goal;
    if (mutation.tasks) this.intentDoc.tasks = mutation.tasks;
    this.intentDoc.version += 1;
    return this.intentDoc;
  }
}
