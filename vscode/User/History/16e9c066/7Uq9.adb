with Expr_Eval; use Expr_Eval;

procedure Ex3 is
   E2 : Expr_Access :=
      new Let'
        ("Ab", new Literal'(Val => 12),
         new Bin_Op'(K => Add,
                     L => new Literal'(Val => 12),
                     R => new Ref'(Ref => "Ab")));
begin
   null;
end Ex3;
