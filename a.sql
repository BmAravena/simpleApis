CREATE OR REPLACE PROCEDURE saludar_usuario (
p_nombre IN VARCHAR2 ) AS
BEGIN
    DBMS_OUTPUT.PUT_LINE('¡Hola, ' || p_nombre || '! Bienvenido/a.');
END;
/


EXEC saludar_usuario('Benjamín');



























SET VERIFY OFF
DECLARE
    v_grade CHAR(1) := UPPER('&grade');
    v_appraisal VARCHAR2(20);
BEGIN
    v_appraisal := CASE v_grade
        WHEN 'A' THEN 'Excellent'
        WHEN 'B' THEN 'Very Good'
        WHEN 'C' THEN 'Good'
        ELSE 'No such grade'
    END;
DBMS_OUTPUT.PUT_LINE ('Grade: '|| v_grade || 'Appraisal' || v_appraisal'')
END;
/