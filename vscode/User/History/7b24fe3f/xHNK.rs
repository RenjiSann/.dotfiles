#[derive(Debug)]
enum Operator {
    Plus,
    Minus,
    Divide,
    Multiply,
}

#[derive(Debug)]
enum Expr {
    BinOp {
        l: Box<Expr>,
        op: Operator,
        r: Box<Expr>,
    },
    IfExpr {
        cond: Box<Expr>,
        true_branch: Box<Expr>,
        false_branch: Box<Expr>,
    },
    Literal(i32),
}

impl Expr {
    fn eval(&self) -> i32 {
        match self {
            Expr::BinOp { l, op, r } => match op {
                Operator::Plus => l.eval() + r.eval(),
                Operator::Minus => l.eval() - r.eval(),
                Operator::Divide => l.eval() / r.eval(),
                Operator::Multiply => l.eval() * r.eval(),
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
    use super::{Expr::*, Operator::*, *};

    #[test]
    fn test_add() {
        let expr = BinOp {
            l: Box::new(Literal(5)),
            op: Plus,
            r: Box::new(Literal(3)),
        };
        assert_eq!(expr.eval(), 8);
    }

    #[test]
    fn test_sub() {
        let expr = BinOp {
            l: Box::new(Literal(5)),
            op: Minus,
            r: Box::new(Literal(7)),
        };
        assert_eq!(expr.eval(), -2);
    }

    #[test]
    fn test_div() {
        let expr = BinOp {
            l: Box::new(Literal(13)),
            op: Divide,
            r: Box::new(Literal(2)),
        };
        assert_eq!(expr.eval(), 6);
    }

    #[test]
    fn test_if() {
        let expr = IfExpr {
            cond: Box::new(Literal(3)),
            true_branch: Box::new(Literal(5)),
            false_branch: Box::new(Literal(8)),
        };
        assert_eq!(eval(&expr), 5);
    }
}