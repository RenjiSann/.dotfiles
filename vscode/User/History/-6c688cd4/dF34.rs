struct SortedList<T>
where T: PartialOrd + Ord {
    vec: Vec<T>
}

impl<T> SortedList<T> {
    pub fn new() -> Self {
        SortedList { vec: vec![] }
    }
}