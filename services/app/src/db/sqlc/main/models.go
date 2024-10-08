// Code generated by sqlc. DO NOT EDIT.
// versions:
//   sqlc v1.27.0

package sqlcmain

import (
	"database/sql"
)

type Face struct {
	ID       int64  `json:"id"`
	PersonID int32  `json:"person_id"`
	Path     string `json:"path"`
}

type Person struct {
	ID        int64        `json:"id"`
	Prime     string       `json:"prime"`
	FirstName string       `json:"first_name"`
	LastName  string       `json:"last_name"`
	CreatedAt sql.NullTime `json:"created_at"`
}

type Result struct {
	ID            int64   `json:"id"`
	SessionID     int32   `json:"session_id"`
	PersonID      int32   `json:"person_id"`
	ThumbnailPath string  `json:"thumbnail_path"`
	Similarity    float64 `json:"similarity"`
}

type Session struct {
	ID        int64        `json:"id"`
	Prime     string       `json:"prime"`
	VideoPath string       `json:"video_path"`
	CreatedAt sql.NullTime `json:"created_at"`
	EndedAt   sql.NullTime `json:"ended_at"`
}
