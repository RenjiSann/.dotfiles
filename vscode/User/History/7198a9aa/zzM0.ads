package Stack is
   Max : constant Natural := 2;

   type Element_T is new Natural;
   type Stack_T is private;

   procedure Reset (S : out Stack_T);
   function  Pop (S : in out Stack_T) return Element_T;
   procedure Push (S : in out Stack_T; E : Element_T);

   function Is_Full (S : in Stack_T) return Boolean is (S'Length = Max);
   function Is_Empty (S : in Stack_T) return Boolean is (S'Length = 0);

private
   type Element_Array_T is array (Positive range 1 .. Max) of Element_T;
   type Stack_T is record
      Content : Element_Array_T;
      Length  : Natural := 0;
   end record;
end Stack;
