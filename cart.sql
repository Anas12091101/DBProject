BEGIN;
--
-- Create model Cart
--
CREATE TABLE "cart_cart" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "profile_id" bigint NOT NULL UNIQUE REFERENCES "User_profile" ("id") DEFERRABLE INITIALLY DEFERRED, "price" integer unsigned NULL CHECK ("price" >= 0));
--
-- Create model CartProduct
--
CREATE TABLE "cart_cartproduct" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "quantity" integer unsigned NOT NULL CHECK ("quantity" >= 0), "cart_id" bigint NOT NULL REFERENCES "cart_cart" ("id") DEFERRABLE INITIALLY DEFERRED, "product_id" bigint NULL REFERENCES "product_product" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "cart_cartproduct_cart_id_55d1af26" ON "cart_cartproduct" ("cart_id");
CREATE INDEX "cart_cartproduct_product_id_7f6785a4" ON "cart_cartproduct" ("product_id");
COMMIT;
