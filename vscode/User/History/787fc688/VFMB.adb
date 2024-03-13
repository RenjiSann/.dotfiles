with Ada.Text_IO; use Ada.Text_IO;

procedure Test_Invert is
    function Invert (S : String) return String is
        reversed : String (S'Range);
    begin
        for I in S'Range loop
            reversed(I) := S(S'Length - I + 1);
        end loop;

        return reversed;
    end Invert;
begin
    Put_Line("testing");
    pragma Assert(Invert("test") = "tset");
    pragma Assert(Invert("") = "", "Empty String not working");
    pragma Assert(False);
    Put_Line("testing done");
end Test_Invert;
