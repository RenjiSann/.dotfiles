pub(crate) fn diagnostic_message(c1: char, c2: char) -> String {
    format!("Character `{}` (U+{:04X}) could be confused with the ASCII character `{}` (U+{:04X})",
            c1, c1 as u32, c2, c2 as u32)
}
