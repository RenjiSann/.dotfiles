with Ada.Text_IO; use Ada.Text_IO;

procedure Exo3 is
   function StrToI(S: String) return Integer is
      ret: Integer := 0;
      neg: Boolean := False;
      SS: String := S'Range;
   begin
      if S = "" then
         return 0;
      end if;

      if S'First = '-' then
         neg := True;
         SS := S(2..S'Length);
      end if;

      for I in SS'Range loop
         ret := ret * 10;
         ret := ret + Character'Pos(S(I)) - Character'Pos('0');
      end loop;

      if neg then
         ret := -ret;
      end if;

      return ret;

   end StrToI;
begin
   Put_Line(StrToI("5")'Image);
   Put_Line(StrToI("123")'Image);
   Put_Line(StrToI("0")'Image);
   Put_Line(StrToI("-10")'Image);
end Exo3;
