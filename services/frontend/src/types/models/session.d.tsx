

export interface Session {
    id: number;
    prime: string;
    video_path: string;
    created_at: { Time: string, Valid: boolean };
    ended_at: { Time: string, Valid: boolean };
}