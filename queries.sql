/* Anak A1L */
SELECT f1.id, f1.name, f1.sex, f1.parent
FROM family_node AS f1
WHERE f1.parent=1;

/* Cucu A1L */
SELECT f1.id, f1.name, f1.sex, f1.parent
FROM family_node AS f1
WHERE f1.parent IN (
	SELECT f2.id
	FROM family_node AS f2
	WHERE f2.parent=1
);

/* Cucu perempuan A1L */
SELECT f1.id, f1.name, f1.sex, f1.parent
FROM family_node AS f1
WHERE f1.parent IN (
	SELECT f2.id
	FROM family_node AS f2
	WHERE f2.parent=1
) AND f1.sex, f1.parent='P';

/* Bibi C2P */
SELECT f1.id, f1.name, f1.sex, f1.parent
FROM family_node AS f1
WHERE f1.parent=(
	SELECT f2.parent
	FROM family_node AS f2
	WHERE f2.id=(
		SELECT f3.parent
		FROM family_node AS f3
		WHERE f3.id=7
	)
) AND f1.sex, f1.parent='P';


/* Sepupu laki-laki E1P */
SELECT f1.id, f1.name, f1.sex, f1.parent
FROM family_node AS f1
WHERE f1.parent IN (
	SELECT f2.id
	FROM family_node AS f2
	WHERE f2.parent=(
		SELECT f3.parent
		FROM family_node AS f3
		WHERE f3.id=(
			SELECT f4.parent
			FROM family_node AS f4
			WHERE f4.id=10
		)
	)
) AND f1.sex, f1.parent='L';
