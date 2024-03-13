with Expr_Eval; use Expr_Eval;

procedure Ex2 is
  div_0 : Expr_Access :=
   new Bin_Op'
    (op => Div, L => new Literal'(Val => 12), R => new Literal'(Val => 0));

  E1 : Expr_Access :=
   new Bin_Op'
    (op => Add, L => new Literal'(Val => 12), R => new Literal'(Val => 15));

  E2 : Expr_Access := new If_Expr'(
    Cond => new Literal'(Val => 12),
    True_Branch => new Literal'(Val => 44),
    False_Branch => new Literal'(Val => 45)
  );

  E_debranching_and : Expr_Access := new Bin_Op'(
    op => Logic_And,
    L => new Literal'(Val => 1),
    R => div_0
  );

  E_debranching_or : Expr_Access := new Bin_Op'(
    op => Logic_Or,
    L => new Literal'(Val => 1),
    R => div_0
    );
begin
  pragma Assert (E1.Eval = 27);
  pragma Assert (E2.Eval = 44);
  pragma Assert (E_debranching_and.Eval = 0);
  pragma Assert (E_debranching_or.Eval = 1);
end Ex2;
