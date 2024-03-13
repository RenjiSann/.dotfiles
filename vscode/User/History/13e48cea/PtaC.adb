package body Expr_Eval is

    function DispatchOp(op: Op_Kind; left: Expr; right: Expr) return Integer is
    begin
        case op is
            when Add => return Eval(left) + Eval(right);
            when Sub => return Eval(left) - Eval(right);
            when Mul => return Eval(left) * Eval(right);
            when Div => return Eval(left) / Eval(right);
            when Logic_And => return Eval(left) / Eval(right);
            when Logic_Or => return Eval(left) / Eval(right);
        end case;
    end DispatchOp;

    function Eval (E: Expr) return Integer is
    begin
        case E.Kind is
            when Literal => return Expr.Val;
            when Bin_Op
        end case;
    end Eval;

end Expr_Eval;