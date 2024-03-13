with Ada.Text_IO; use Ada.Text_IO;
with IntStack; use IntStack;

procedure Exo8 is
   n: Integer;
   my_stack: Stack;
   my_other_stack: Stack;
begin
   IntStack.Push(my_stack, 10);
   IntStack.Push(my_stack, 12);
   IntStack.Push(my_other_stack, 4453);
   IntStack.Push(my_stack, 40);

   IntStack.Pop(my_stack, n);
   Put_Line(Integer'Image(n));
   IntStack.Pop(my_other_stack, n);
   Put_Line(Integer'Image(n));
   IntStack.Pop(my_stack, n);
   Put_Line(Integer'Image(n));
   IntStack.Pop(my_stack, n);
   Put_Line(Integer'Image(n));

   -- Should raise a constraint error
   IntStack.Pop(my_other_stack, n);
end Exo8;
