-- name: CreateResult :one
INSERT INTO "Result"(
                     session_id,
                     person_id,
                     thumbnail_path,
                     similarity
) VALUES ($1, $2, $3, $4) RETURNING *;


-- name: GetResultListBySessionId :many
SELECT * FROM "Result" WHERE session_id=$1 ORDER BY id DESC LIMIT $2 OFFSET $3;

-- name: GetResultListByPersonId :many
SELECT * FROM "Result" WHERE session_id=$1 ORDER BY id DESC LIMIT $2 OFFSET $3;


