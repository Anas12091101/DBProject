BEGIN;
--
-- Create model testclass
--
-- CREATE TABLE "product_testclass" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "img" text NOT NULL);
--
-- Create model Category
--
CREATE TABLE "product_category" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(200) NOT NULL, "created_at" datetime NOT NULL);
--
-- Create model Product
--
CREATE TABLE "product_product" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(200) NOT NULL, "price" integer NOT NULL, "primary_image" varchar(100) NULL, "categoryId_id" bigint NOT NULL REFERENCES "product_category" ("id") DEFERRABLE INITIALLY DEFERRED, "description" text NULL, "in_stock" integer NOT NULL);
--
-- Create model imgSrc
--
CREATE TABLE "product_imgsrc" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "url" varchar(100) NULL, "product_id" bigint NOT NULL REFERENCES "product_product" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "product_product_categoryId_id_87615990" ON "product_product" ("categoryId_id");
CREATE INDEX "product_imgsrc_product_id_1e7a90d9" ON "product_imgsrc" ("product_id");
COMMIT;
