with Expr_Eval; use Expr_Eval;
with Ada.Text_IO; use Ada.Text_IO;

procedure Ex1 is
    E1 : Expr := (Kind => Bin_Op,
                 L => new Expr'(Kind => Literal, Val => 12),
                 R => new Expr'(Kind => Literal, Val => 15),
                 Op => Add);
    E2 : Expr := (Kind      => If_Expr,
                  Cond      => new Expr'(Kind => Literal, Val => 12),
                  Then_Expr => new Expr'(Kind => Literal, Val => 44),
                  Else_Expr => new Expr'(Kind => Literal, Val => 44),
    );
begin
    Put_Line (Eval (E)'Image);
    pragma Assert(Eval(E), 27);
end Ex1;