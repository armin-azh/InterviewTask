-- name: CreatePerson :one
INSERT INTO "Person"(
    prime,
    first_name,
    last_name
)VALUES (
    $1, $2, $3
) RETURNING *;


-- name: GetPersonList :many
SELECT * FROM "Person"
ORDER BY id
LIMIT $1 OFFSET $2;