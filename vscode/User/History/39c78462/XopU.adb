with Expr_Eval; use Expr_Eval;
with Ada.Text_IO; use Ada.Text_IO;

procedure Ex1 is
    E : Expr := (Kind => Bin_Op,
                 L => new Expr'(Kind => Literal, Val => 12),
                 R => new Expr'(Kind => Literal, Val => 15),
                 Op => Add);
begin
    Put_Line (Eval (E)'Image);
end Ex1;