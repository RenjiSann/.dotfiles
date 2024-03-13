with Ada.Text_IO; use Ada.Text_IO;

procedure Test_Invert is
    function Invert (S : String) return String is is
        reversed : String := S;
    begin
        for I in S'Length loop
            reversed(I) := S(S'Length - I - 1);
        end loop;

        return reversed;
    end Invert;
begin
    if Invert("test") /= "tset" then
        ass;
    end if;
end Test_Invert;