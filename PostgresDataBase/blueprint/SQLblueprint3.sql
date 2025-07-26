CREATE TABLE "users" (
	"id" SERIAL NOT NULL UNIQUE,
	"tg_id" TEXT,
	"name" TEXT,
	PRIMARY KEY("id")
);




CREATE TABLE "notifications" (
	"id" SERIAL NOT NULL UNIQUE,
	"user_id" INTEGER,
	"text" TEXT,
	"date" TIMESTAMP,
	"sent" BOOLEAN,
	PRIMARY KEY("id")
);



ALTER TABLE "notifications"
ADD FOREIGN KEY("user_id") REFERENCES "users"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;