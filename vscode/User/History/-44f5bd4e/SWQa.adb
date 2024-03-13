with Ada.Text_IO; use Ada.Text_IO;
with IntStack;

procedure Exo6 is
   n: Integer;
begin
   IntStack.Push(10);
   IntStack.Push(12);
   IntStack.Push(40);

   IntStack.Pop(n);
   Put_Line(Integer'Image(n));
   IntStack.Pop(n);
   Put_Line(Integer'Image(n));
   IntStack.Pop(n);
   Put_Line(Integer'Image(n));
   IntStack.Pop(n);
end Exo6;
