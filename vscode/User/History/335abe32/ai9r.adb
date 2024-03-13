procedure Exo2 is
   function ItoStr(I: Integer) return String is
      ret: String (1 .. 21);
      digit: Integer;
      index: Integer := 21;
   begin
      while I /= 0 loop
         digit := I mod 10;
         ret(index) := Character'Val(Character'Pos('0') + digit);
         index := index + 1;
      end loop;
   end ItoStr;
begin
   pragma Assert(ItoStr(5) = "5");
end Exo2;
