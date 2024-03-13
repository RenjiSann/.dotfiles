with Ada.Text_IO; use Ada.Text_IO;

procedure Test_Invert_2 is
    function Invert (S : in out String) return String is
        A: Character;
        B: Character;
    begin
        for I in 1 .. S'Length / 2 loop
            A := S(I);
            B := S(S'Length - I + 1);
            S(I) := B;
            S(S'Length - I + 1) := A;
        end loop;

        return reversed;
    end Invert;

    SS : String := "Test";
begin
    Invert(SS);
    pragma Assert(SS = "tset");
    pragma Assert(Invert("") = "", "Empty String not working");
end Test_Invert_2;