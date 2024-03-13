with Stack; use Stack;

procedure Main is

   S : Stack_T;
   E : Element_T;
begin

   -- E := Pop (S);
   Push (S, 1);
   Push (S, 1);
   Push (S, 1);
   Push (S, 1);
   E := Pop (S);
   E := Pop (S);
   E := Pop (S);


end Main;
