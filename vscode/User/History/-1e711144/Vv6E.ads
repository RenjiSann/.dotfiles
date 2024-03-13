package Expr_Eval is

    type Expr;

    type Op_Kind is (Add, Sub, Mul, Div, Logic_And, Logic_Or);
    type Expr_Access is access Expr'Class;

    type Expr is abstract tagged null record;
    function Eval (E: Expr) return Integer is abstract;

    type Bin_Op is new Expr with record
        op : Op_Kind;
        L, R : Expr_Access;
    end record;
    overriding function Eval (B : Bin_Op) return Integer;

    type If_Expr is new Expr with record

    end record;
    overriding function Eval (I : If_Expr) return Integer;

    type Literal is new Expr with record
        Val : Integer;
    end record;
    overriding function Eval (L : Literal) return Integer;

end Expr_Eval;
