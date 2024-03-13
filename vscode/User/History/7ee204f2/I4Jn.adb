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

   -- Push to many items
   IntStack.Push(my_stack_ptr.all, 0);
   IntStack.Push(my_stack_ptr.all, 1);
   IntStack.Push(my_stack_ptr.all, 2);
   IntStack.Push(my_stack_ptr.all, 3);
   IntStack.Push(my_stack_ptr.all, 4);
   IntStack.Push(my_stack_ptr.all, 5);
   IntStack.Push(my_stack_ptr.all, 6);
   IntStack.Push(my_stack_ptr.all, 7);
   IntStack.Push(my_stack_ptr.all, 8);
   IntStack.Push(my_stack_ptr.all, 9);
   -- This will crash
   IntStack.Push(my_stack_ptr.all, 9);
end Exo8;
