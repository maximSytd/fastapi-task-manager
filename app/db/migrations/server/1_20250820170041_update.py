from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" DROP CONSTRAINT IF EXISTS "fk_user_grade_392bc54a";
        CREATE TABLE IF NOT EXISTS "task" (
    "created" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "modified" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "id" UUID NOT NULL PRIMARY KEY,
    "title" VARCHAR(120) NOT NULL,
    "description" TEXT,
    "status" VARCHAR(11) NOT NULL DEFAULT 'Created',
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "task"."status" IS 'CREATED: Created\nIN_PROGRESS: In progress\nCOMPLETE: Complete';
COMMENT ON TABLE "task" IS 'Represent Task in db.';
        ALTER TABLE "user" DROP COLUMN "grade_id";
        ALTER TABLE "user" DROP COLUMN "is_admin";
        DROP TABLE IF EXISTS "performancereview";
        DROP TABLE IF EXISTS "specialty";
        DROP TABLE IF EXISTS "grade";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ADD "grade_id" INT;
        ALTER TABLE "user" ADD "is_admin" BOOL NOT NULL DEFAULT False;
        DROP TABLE IF EXISTS "task";
        ALTER TABLE "user" ADD CONSTRAINT "fk_user_grade_392bc54a" FOREIGN KEY ("grade_id") REFERENCES "grade" ("id") ON DELETE SET NULL;"""
