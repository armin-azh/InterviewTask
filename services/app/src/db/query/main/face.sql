-- name: CreateNewFace :one
INSERT INTO "Face"(
   person_id,
   path
)VALUES (
$1, $2
) RETURNING *;