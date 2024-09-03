CREATE TABLE "Person" (
                          "id" BIGSERIAL PRIMARY KEY,
                          "prime" varchar(255) UNIQUE NOT NULL,
                          "first_name" varchar(255) NOT NULL,
                          "last_name" varchar(255) NOT NULL,
                          "created_at" timestamptz DEFAULT (now())
);

CREATE TABLE "Face" (
                        "id" BIGSERIAL PRIMARY KEY,
                        "person_id" int NOT NULL,
                        "path" varchar(255) NOT NULL
);

CREATE TABLE "Session" (
                           "id" BIGSERIAL PRIMARY KEY,
                           "prime" varchar(255) UNIQUE NOT NULL,
                           "video_path" varchar(1024) NOT NULL,
                           "created_at" timestamptz DEFAULT (now()),
                           "ended_at" timestamptz
);

CREATE TABLE "Result" (
                          "id" BIGSERIAL PRIMARY KEY,
                          "session_id" int NOT NULL,
                          "person_id" int NOT NULL,
                          "thumbnail_path" char NOT NULL,
                          "similarity" float NOT NULL
);

ALTER TABLE "Face" ADD FOREIGN KEY ("person_id") REFERENCES "Person" ("id") ON DELETE CASCADE;

ALTER TABLE "Result" ADD FOREIGN KEY ("session_id") REFERENCES "Session" ("id") ON DELETE CASCADE;

ALTER TABLE "Result" ADD FOREIGN KEY ("person_id") REFERENCES "Person" ("id") ON DELETE CASCADE;