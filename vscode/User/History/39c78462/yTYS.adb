with Expr_Eval;   use Expr_Eval;
with Ada.Text_IO; use Ada.Text_IO;

procedure Ex1 is
   div_0 : Expr_Access :=
     new Expr'
       (Kind => Bin_Op, L => new Expr'(Kind => Literal, Val => 1),
        R    => new Expr'(Kind => Literal, Val => 0), Op => Div);

   E1                : Expr :=
     (Kind => Bin_Op, L => new Expr'(Kind => Literal, Val => 12),
      R    => new Expr'(Kind => Literal, Val => 15), Op => Add);

   E2                : Expr :=
     (Kind      => If_Expr, Cond => new Expr'(Kind => Literal, Val => 12),
      Then_Expr => new Expr'(Kind => Literal, Val => 44),
      Else_Expr => new Expr'(Kind => Literal, Val => 45));

   E_debranching_and : Expr :=
     (Kind => Bin_Op, L => new Expr'(Kind => Literal, Val => 0), R => div_0,
      Op   => Logic_And);

   E_debranching_or : Expr :=
     (Kind => Bin_Op, L => new Expr'(Kind => Literal, Val => 1), R => div_0,
      Op   => Logic_Or);
begin
   pragma Assert (Eval (E1) = 27);
   pragma Assert (Eval (E2) = 44);
   pragma Assert (Eval (E_debranching_and) = 0);
   pragma Assert (Eval (E_debranching_or) = 1);
end Ex1;
