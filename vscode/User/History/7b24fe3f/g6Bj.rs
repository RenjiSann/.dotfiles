#[derive(Debug)]
enum Operator {
Plus, Minus, Divide, Multiply
}

#[derive(Debug)]
enum Expr {
BinOp { l: Box<Expr>, op: Operator, r: Box<Expr> },
IfExpr { cond: Box<Expr>, true_branch: Box<Expr>, false_branch: Box<Expr> },
Literal(i32)
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
