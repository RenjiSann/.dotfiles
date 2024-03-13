with Expr_Eval; use Expr_Eval;

procedure Ex2 is
  div_0 : Expr_Access :=
   new Bin_Op'
    (op => Div, L => new Literal'(Val => 12), R => new Literal'(Val => 0));

  E1 : Expr_Access :=
   new Bin_Op'
    (op => Add, L => new Literal'(Val => 12), R => new Literal'(Val => 15));

  E2 : Expr :=
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
  pragma Assert (E1.Eval = 27);
  pragma Assert (Eval (E2) = 44);
  pragma Assert (Eval (E_debranching_and) = 0);
  pragma Assert (Eval (E_debranching_or) = 1);
end Ex2;
