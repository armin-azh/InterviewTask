// Code generated by sqlc. DO NOT EDIT.
// versions:
//   sqlc v1.27.0

package sqlcmain

import (
	"context"
	"database/sql"
)

type Querier interface {
	CreateNewFace(ctx context.Context, personID int32, path string) (Face, error)
	CreatePerson(ctx context.Context, prime string, firstName string, lastName string) (Person, error)
	CreateResult(ctx context.Context, sessionID int32, personID int32, thumbnailPath string, similarity float64) (Result, error)
	CreateSession(ctx context.Context, prime string, videoPath string) (Session, error)
	GetPersonByPrime(ctx context.Context, prime string) (Person, error)
	GetPersonList(ctx context.Context, limit int32, offset int32) ([]Person, error)
	GetResultListByPersonId(ctx context.Context, sessionID int32, limit int32, offset int32) ([]Result, error)
	GetResultListBySessionId(ctx context.Context, sessionID int32, limit int32, offset int32) ([]Result, error)
	GetSessionByPrime(ctx context.Context, prime string) (Session, error)
	GetSessionList(ctx context.Context, limit int32, offset int32) ([]Session, error)
	UpdateSessionEndTime(ctx context.Context, endedAt sql.NullTime, iD int64) (Session, error)
}

var _ Querier = (*Queries)(nil)
