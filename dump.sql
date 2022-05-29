-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               PostgreSQL 10.4, compiled by Visual C++ build 1800, 32-bit
-- Server OS:                    
-- HeidiSQL Version:             12.0.0.6468
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES  */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Dumping structure for table public.family_node
DROP TABLE IF EXISTS "family_node";
CREATE TABLE IF NOT EXISTS "family_node" (
	"id" SERIAL NOT NULL,
	"name" VARCHAR(50) NOT NULL,
	"sex" CHAR(1) NOT NULL,
	"parent" INTEGER NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "FK_PARENT" FOREIGN KEY ("parent") REFERENCES "family_node" ("id") ON UPDATE CASCADE ON DELETE CASCADE
);

-- Dumping data for table public.family_node: 0 rows
DELETE FROM "family_node";
/*!40000 ALTER TABLE "family_node" DISABLE KEYS */;
INSERT INTO "family_node" ("name", "sex", "parent") VALUES
	('A1L', 'L', NULL),
	('B1L', 'L', 1),
	('B2L', 'L', 1),
	('B3L', 'L', 1),
	('B4P', 'P', 1),
	('C1L', 'L', 2),
	('C2P', 'P', 2),
	('D1L', 'L', 3),
	('D2L', 'L', 3),
	('E1P', 'P', 4),
	('E2P', 'P', 4);
/*!40000 ALTER TABLE "family_node" ENABLE KEYS */;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
