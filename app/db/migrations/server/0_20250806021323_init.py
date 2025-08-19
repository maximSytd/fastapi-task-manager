from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "specialty" (
    "created" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "modified" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(120) NOT NULL
);
COMMENT ON TABLE "specialty" IS 'Represent Specialty in db.';
CREATE TABLE IF NOT EXISTS "grade" (
    "created" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "modified" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(120) NOT NULL,
    "salary" DECIMAL(7,2) NOT NULL,
    "next_grade_id" INT REFERENCES "grade" ("id") ON DELETE CASCADE,
    "specialty_id" INT NOT NULL REFERENCES "specialty" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "grade" IS 'Represent Grade in db.';
CREATE TABLE IF NOT EXISTS "user" (
    "created" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "modified" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(64) NOT NULL UNIQUE,
    "password_hash" VARCHAR(128) NOT NULL,
    "is_admin" BOOL NOT NULL DEFAULT False,
    "grade_id" INT REFERENCES "grade" ("id") ON DELETE SET NULL
);
COMMENT ON TABLE "user" IS 'Represent User in db.';
CREATE TABLE IF NOT EXISTS "performancereview" (
    "created" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "modified" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "date_held" TIMESTAMPTZ NOT NULL,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "performancereview" IS 'Represent Performance review in db.';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
