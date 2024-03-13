package body Expr_Eval is

    function DispatchOp(op: Op_Kind; left: Expr; right: Expr) return Integer is
    begin
    end DispatchOp;

    function Eval (E: Expr) return Integer is
    begin
        case E.Kind is
            when Literal => return Expr.Val;
            when Bin_Op
        end case;
    end Eval;

end Expr_Eval;