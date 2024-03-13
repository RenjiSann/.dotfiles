with Ada.Containers.Indefinite_Hashed_Maps;
with Ada.Strings.Hash;

package Expr_Eval is
    package Integer_Hashed_Maps is new
        Ada.Containers.Indefinite_Hashed_Maps
        (Key_Type        => String,
            Element_Type    => Integer,
            Hash            => Ada.Strings.Hash,
            Equivalent_Keys => "=");

    type Expr;

    type Op_Kind is (Add, Sub, Mul, Div, Logic_And, Logic_Or);
    type Expr_Access is access Expr'Class;

    type Expr is abstract tagged record
        
    end record;
    function Eval (E: Expr) return Integer is abstract;

    type Bin_Op is new Expr with record
        op : Op_Kind;
        L, R : Expr_Access;
    end record;
    overriding function Eval (B : Bin_Op) return Integer;

    type If_Expr is new Expr with record
        Cond, True_Branch, False_Branch : Expr_Access;
    end record;
    overriding function Eval (I : If_Expr) return Integer;

    type Literal is new Expr with record
        Val : Integer;
    end record;
    overriding function Eval (L : Literal) return Integer;

    subtype Var_Name is String (1 .. 2);
    type Let is new Expr with record
       Bind        : Var_Name;
       Bound_Value : Expr_Access;
       Target_Expr : Expr_Access;
    end record;
    overriding function Eval (L : Let) return Integer;

    type Ref is new Expr with record
       Ref : Var_Name;
    end record;
    overriding function Eval (R : Ref) return Integer;

end Expr_Eval;
