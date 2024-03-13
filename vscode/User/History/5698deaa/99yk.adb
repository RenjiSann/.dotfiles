with Ada.Text_IO; use Ada.Text_IO;

procedure Test_Invert_2 is
    procedure Invert (S : in out String) is
        A: Character;
        B: Character;
    begin
        for I in 1 .. S'Length / 2 loop
            A := S(I);
            B := S(S'Length - I + 1);
            S(I) := B;
            S(S'Length - I + 1) := A;
        end loop;
    end Invert;

    S1 : String := "Test";
    S2 : String := "";
begin
    Invert(S1);
    pragma Assert(S1 = "tset");
    Invert(S2);
    pragma Assert(S2 = "");
end Test_Invert_2;