with Ada.Text_IO; use Ada.Text_IO;

procedure Exo3 is
   function StrToI(S: String) return Integer is
      ret: Integer := 0;
   begin
      for I in S'Range loop
         ret := ret * 10;
         ret := ret + Character'Pos(S(I)) - Character'Pos('0');
      end loop;
      return ret;

   end StrToI;
begin
   Put_Line(StrToI("5")'Image);
end Exo3;
