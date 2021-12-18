BEGIN;
--
-- Create model Order
--
CREATE TABLE "orders_order" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "status" varchar(200) NULL, "total_price" integer unsigned NULL CHECK ("total_price" >= 0), "owner_id" bigint NOT NULL REFERENCES "User_profile" ("id") DEFERRABLE INITIALLY DEFERRED, "created_at" datetime NULL);
--
-- Create model OrderProduct
--
CREATE TABLE "orders_orderproduct" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "quantity" integer unsigned NOT NULL CHECK ("quantity" >= 0), "Order_id" bigint NOT NULL REFERENCES "orders_order" ("id") DEFERRABLE INITIALLY DEFERRED, "product_id" bigint NOT NULL REFERENCES "product_product" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "orders_order_owner_id_b000b586" ON "orders_order" ("owner_id");
CREATE INDEX "orders_orderproduct_Order_id_9a40c570" ON "orders_orderproduct" ("Order_id");
CREATE INDEX "orders_orderproduct_product_id_4d6ac024" ON "orders_orderproduct" ("product_id");
COMMIT;
