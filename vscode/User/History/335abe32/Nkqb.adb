procedure Exo2 is
   function ItoStr(I: Integer) return String is
      ret: String (1 .. 21);
   begin
      while I /= 0 loop
      end loop;
   end ItoStr;
begin
   pragma Assert(ItoStr(5) = "5");
end Exo2;
