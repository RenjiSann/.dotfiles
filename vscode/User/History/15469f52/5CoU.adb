procedure Exo3 is
begin
   function StrToI(S: String) return Integer is
      ret: Integer := 0;
   begin
      for I in S'Range loop
         ret := ret * 10;
         ret := ret + Character'Pos(S(I)) - Character'Pos('0');
      end loop;
      return ret;

   end StrToI;

   Put_Line(StrToI("5")'Image);
end Exo3;
