with Ada.Text_IO; use Ada.Text_IO;

procedure Exo2 is
   function ItoStr(N: Integer) return String is
      ret: String (1 .. 21);
      digit: Integer;
      index: Integer := 21;
      I: Integer := N;
      Neg: Boolean;
   begin
      if I = 0 then
         return "0";
      end if;

      if I < 0 then
         Put_Line("number under 0");
         I := -I;
         Neg := True;
      end if;

      while I /= 0 loop
         digit := I mod 10;
         ret(index) := Character'Val(Character'Pos('0') + digit);
         index := index - 1;
         I := I / 10;
      end loop;

      if Neg then
         ret(index) := '-';
         index := index - 1;
      end if;

      return ret(index .. 21);

   end ItoStr;
begin
   Put_Line(ItoStr(5));
   Put_Line(ItoStr(455));
   Put_Line(ItoStr(0));
   Put_Line(ItoStr(-10));
end Exo2;
