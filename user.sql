BEGIN;
--
-- Create model Profile
--
CREATE TABLE "User_profile" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "is_verified" bool NOT NULL, "user_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "city" varchar(50) NULL, "phoneno" varchar(50) NULL);
COMMIT;
