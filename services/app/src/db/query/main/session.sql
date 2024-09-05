-- name: CreateSession :one
INSERT INTO "Session"(
                      prime,
                      video_path
) VALUES ($1, $2) RETURNING *;


-- name: GetSessionList :many
SELECT * FROM "Session" ORDER BY id LIMIT $1 OFFSET $2;

-- name: GetSessionByPrime :one
SELECT * FROM "Session" WHERE prime = $1 LIMIT 1;
