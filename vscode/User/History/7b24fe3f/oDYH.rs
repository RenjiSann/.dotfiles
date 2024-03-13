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

pub fn eval(expr: &Expr) -> i32 {
    match expr {
        Expr::BinOp { l, op, r } => {
            match op {
                Operator::Plus => eval(l) + eval(r),
                Operator::Minus => eval(l) - eval(r),
                Operator::Divide => eval(l) / eval(r),
                Operator::Multiply => eval(l) * eval(r),
            }
        }
        Expr::IfExpr { cond, true_branch, false_branch } => {
            if eval(cond) != 0 {
                eval(true_branch)
            } else {
                eval(&false_branch)
            }
        }
        Expr::Literal(x) => *x,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let result = add(2, 2);
        assert_eq!(result, 4);
    }
}
