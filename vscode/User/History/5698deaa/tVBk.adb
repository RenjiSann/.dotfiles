with Ada.Text_IO; use Ada.Text_IO;

procedure Test_Invert_2 is
    function Invert (S : in out String) return String is
        reversed : String(S'Range);
    begin
        for I in S'Range loop
            reversed(I) := S(S'Length - I + 1);
        end loop;

        return reversed;
    end Invert;
begin
    pragma Assert(Invert("test") = "tset");
    pragma Assert(Invert("") = "", "Empty String not working");
end Test_Invert_2;