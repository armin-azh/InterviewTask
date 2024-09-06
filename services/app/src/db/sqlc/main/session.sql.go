// Code generated by sqlc. DO NOT EDIT.
// versions:
//   sqlc v1.27.0
// source: session.sql

package sqlcmain

import (
	"context"
	"database/sql"
)

const createSession = `-- name: CreateSession :one
INSERT INTO "Session"(
                      prime,
                      video_path
) VALUES ($1, $2) RETURNING id, prime, video_path, created_at, ended_at
`

func (q *Queries) CreateSession(ctx context.Context, prime string, videoPath string) (Session, error) {
	row := q.db.QueryRowContext(ctx, createSession, prime, videoPath)
	var i Session
	err := row.Scan(
		&i.ID,
		&i.Prime,
		&i.VideoPath,
		&i.CreatedAt,
		&i.EndedAt,
	)
	return i, err
}

const getSessionByPrime = `-- name: GetSessionByPrime :one
SELECT id, prime, video_path, created_at, ended_at FROM "Session" WHERE prime = $1 LIMIT 1
`

func (q *Queries) GetSessionByPrime(ctx context.Context, prime string) (Session, error) {
	row := q.db.QueryRowContext(ctx, getSessionByPrime, prime)
	var i Session
	err := row.Scan(
		&i.ID,
		&i.Prime,
		&i.VideoPath,
		&i.CreatedAt,
		&i.EndedAt,
	)
	return i, err
}

const getSessionList = `-- name: GetSessionList :many
SELECT id, prime, video_path, created_at, ended_at FROM "Session" ORDER BY id DESC LIMIT $1 OFFSET $2
`

func (q *Queries) GetSessionList(ctx context.Context, limit int32, offset int32) ([]Session, error) {
	rows, err := q.db.QueryContext(ctx, getSessionList, limit, offset)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var items []Session
	for rows.Next() {
		var i Session
		if err := rows.Scan(
			&i.ID,
			&i.Prime,
			&i.VideoPath,
			&i.CreatedAt,
			&i.EndedAt,
		); err != nil {
			return nil, err
		}
		items = append(items, i)
	}
	if err := rows.Close(); err != nil {
		return nil, err
	}
	if err := rows.Err(); err != nil {
		return nil, err
	}
	return items, nil
}

const updateSessionEndTime = `-- name: UpdateSessionEndTime :one
UPDATE "Session" SET ended_at = $1 WHERE id = $2 RETURNING id, prime, video_path, created_at, ended_at
`

func (q *Queries) UpdateSessionEndTime(ctx context.Context, endedAt sql.NullTime, iD int64) (Session, error) {
	row := q.db.QueryRowContext(ctx, updateSessionEndTime, endedAt, iD)
	var i Session
	err := row.Scan(
		&i.ID,
		&i.Prime,
		&i.VideoPath,
		&i.CreatedAt,
		&i.EndedAt,
	)
	return i, err
}
