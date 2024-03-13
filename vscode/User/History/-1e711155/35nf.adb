package body Expr_Eval is

    overriding function Eval (B : Bin_Op) return Integer is
    begin
        case B.op is
            when Add =>
                return Eval (B.L) + Eval (B.R);
            when Sub =>
                return Eval (B.L) - Eval (B.R);
            when Mul =>
                return Eval (B.L) * Eval (B.R);
            when Div =>
                return Eval (B.L) / Eval (B.R);
            when Logic_And =>
                if Eval (B.L) = 0 or else Eval (B.R) = 0 then
                    return 0;
                else
                    return 1;
                end if;
            when Logic_Or =>
                if Eval (B.L) = 1 or else Eval (B.R) = 1 then
                    return 1;
                else
                    return 0;
                end if;
        end case;
    end Eval;

    overriding function Eval (I : If_Expr) return Integer is
    begin
        if Eval(E.Cond.all) /= 0 then
            return Eval(E.Then_Expr.all);
        else
            return Eval(E.Else_Expr.all);
        end if;
    end Eval;

    overriding function Eval (L : Literal) return Integer is
    begin
        return L.Val;
    end Eval;

end Expr_Eval;
