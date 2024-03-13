with Ada.Text_IO; use Ada.Text_IO;
with IntStack; use IntStack;

procedure Exo8 is
   n: Integer;
   my_stack_ptr: Stack_Access := new Stack(10);
begin
   IntStack.Push(my_stack_ptr.all, 10);
   IntStack.Push(my_stack_ptr.all, 11);
   IntStack.Push(my_stack_ptr.all, 13);

   IntStack.Pop(my_stack_ptr.all, n);
   Put_Line(Integer'Image(n));
   IntStack.Pop(my_stack_ptr.all, n);
   Put_Line(Integer'Image(n));
   IntStack.Pop(my_stack_ptr.all, n);
   Put_Line(Integer'Image(n));

   -- Should raise a constraint error
   IntStack.Pop(my_stack_ptr.all, n);
end Exo8;
