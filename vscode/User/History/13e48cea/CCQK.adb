package body Expr_Eval is

    function DispatchOp
       (op : Op_Kind; left : Expr; right : Expr) return Integer
    is
    begin
        case op is
            when Add =>
                return Eval (left) + Eval (right);
            when Sub =>
                return Eval (left) - Eval (right);
            when Mul =>
                return Eval (left) * Eval (right);
            when Div =>
                return Eval (left) / Eval (right);
            when Logic_And =>
                if Eval (left) = 0 or else Eval (right) = 0 then
                    return 0;
                else
                    return 1;
                end if;
            when Logic_Or =>
                if Eval (left) = 1 or else Eval (right) = 1 then
                    return 1;
                else
                    return 0;
                end if;
        end case;
    end DispatchOp;

    function Eval (E : Expr) return Integer is
    begin
        case E.Kind is
            when Literal =>
                return E.Val;
            when Bin_Op =>
                return DispatchOp(E.Op, E.L, E.R);
            when If_Expr =>
                if Eval(E.Cond) = 1 then
                    return Eval(E.Then_Expr);
                else
                    return Eval(E.Else_Expr);
                end if;
        end case;
    end Eval;

end Expr_Eval;
