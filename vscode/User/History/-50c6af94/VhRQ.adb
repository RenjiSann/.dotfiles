package body Expr_Eval is

    procedure PopulateVarMap(mapParent : in Map; mapChild : in out Map) is
    begin
        for key in mapParent.Iterate loop
            mapChild.Include(key, mapParent(key));
        end loop;
    end PopulateVarMap;

    overriding function Eval (B : Bin_Op) return Integer is
    begin
        PopulateVarMap(B.Var_Map, B.L.Var_Map);
        PopulateVarMap(B.Var_Map, B.R.Var_Map);
        case B.op is
            when Add =>
                return B.L.Eval + B.R.Eval;
            when Sub =>
                return B.L.Eval - B.R.Eval;
            when Mul =>
                return B.L.Eval * B.R.Eval;
            when Div =>
                return B.L.Eval / B.R.Eval;
            when Logic_And =>
                if B.L.Eval = 0 or else B.R.Eval = 0 then
                    return 0;
                else
                    return 1;
                end if;
            when Logic_Or =>
                if B.L.Eval = 1 or else B.R.Eval = 1 then
                    return 1;
                else
                    return 0;
                end if;
        end case;
    end Eval;

    overriding function Eval (I : If_Expr) return Integer is
    begin
        PopulateVarMap(I.Var_Map, I.Cond.Var_Map);
        if I.Cond.Eval /= 0 then
            PopulateVarMap(I.Var_Map, I.True_Branch.Var_Map);
            return I.True_Branch.Eval;
        else
            PopulateVarMap(I.Var_Map, I.False_Branch.Var_Map);
            return I.False_Branch.Eval;
        end if;
    end Eval;

    overriding function Eval (L : Literal) return Integer is
    begin
        return L.Val;
    end Eval;

    overriding function Eval (L : Let) return Integer is
    begin
        -- Redefine fork bomb
        L.Target_Expr.Var_Map.Include(L.Bind, L.Bound_Value.Eval);
        return L.Target_Expr.Eval;
    end Eval;

    overriding function Eval (R : Ref) return Integer is
    begin
        return R.Var_Map(R.Ref);
    end Eval;

end Expr_Eval;