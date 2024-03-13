with Ada.Text_IO; use Ada.Text_IO;

procedure Test_Invert is
    function Invert (S : String) return String
        reversed : String;
    begin
        for I in S'Length loop
        reversed(I) := S(S'Length - I - 1);
        end loop;
    end Invert;
begin
end Test_Invert;