#[derive(Debug)]
enum ArithOp {
    Plus,
    Minus,
    Divide,
    Multiply,
}

#[derive(Debug)]
enum Expr<'a> {
    BinOp {
        l: &'a Expr<'a>,
        op: ArithOp,
        r: &'a Expr<'a>,
    },
    IfExpr {
        cond: &'a Expr<'a>,
        true_branch: &'a Expr<'a>,
        false_branch: &'a Expr<'a>,
    },
    Literal(i32),
}

impl<'a> Expr<'a> {
    fn eval(&self) -> i32 {
        match self {
            Expr::BinOp { l, op, r } => match op {
                ArithOp::Plus => l.eval() + r.eval(),
                ArithOp::Minus => l.eval() - r.eval(),
                ArithOp::Divide => l.eval() / r.eval(),
                ArithOp::Multiply => l.eval() * r.eval(),
            },
            Expr::IfExpr {
                cond,
                true_branch,
                false_branch,
            } => {
                if cond.eval() != 0 {
                    true_branch.eval()
                } else {
                    false_branch.eval()
                }
            }
            Expr::Literal(x) => *x,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::{Expr::*, ArithOp::*};

    #[test]
    fn test_add() {
        let expr = BinOp {
            l: &Literal(5),
            op: Plus,
            r: &Literal(3),
        };
        assert_eq!(expr.eval(), 8);
    }

    #[test]
    fn test_sub() {
        let expr = BinOp {
            l: &Literal(5),
            op: Minus,
            r: &Literal(7),
        };
        assert_eq!(expr.eval(), -2);
    }

    #[test]
    fn test_mal() {
        let expr = BinOp {
            l: &Literal(-9),
            op: Multiply,
            r: &Literal(7),
        };
        assert_eq!(expr.eval(), -63);
    }

    #[test]
    fn test_div() {
        let expr = BinOp {
            l: &Literal(13),
            op: Divide,
            r: &Literal(2),
        };
        assert_eq!(expr.eval(), 6);
    }

    #[test]
    fn test_if() {
        let expr = IfExpr {
            cond: &Literal(3),
            true_branch: &Literal(5),
            false_branch: &Literal(8),
        };
        assert_eq!(expr.eval(), 5);
    }

    #[test]
    fn test_big() {
        let expr = IfExpr {
            cond: &BinOp {
                l: &Literal(122),
                op: Multiply,
                r: &Literal(4),
            },
            true_branch: &Literal(3),
            false_branch: &Literal(8),
        };
        assert_eq!(expr.eval(), 3);
    }
}
