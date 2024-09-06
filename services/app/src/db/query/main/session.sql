-- name: CreateSession :one
INSERT INTO "Session"(
                      prime,
                      video_path
) VALUES ($1, $2) RETURNING *;


-- name: GetSessionList :many
SELECT * FROM "Session" ORDER BY id DESC LIMIT $1 OFFSET $2;

-- name: GetSessionByPrime :one
SELECT * FROM "Session" WHERE prime = $1 LIMIT 1;

-- name: UpdateSessionEndTime :one
UPDATE "Session" SET ended_at = $1 WHERE id = $2 RETURNING *;
