procedure Exo4 is
    subtype RomanNumber is Natural range 1 .. 3_999;
    subtype Digit is Natural range 0 .. 9;
    -- (I V X)
    -- (X L C)
    -- (C D M)
    function DigitToString
       (d : Digit; c1 : Character; c2 : Character; c3 : Character)
        return String
    is
        ret  : String (1 .. 4);
        size : Integer := 0;
    begin
        case d is
            when 0 =>
                return "";
            when 1 =>
                ret (1) := c1;
                size    := 1;
            when 2 =>
                ret (1) := c1;
                ret (2) := c1;
                size    := 2;
            when 3 =>
                ret (1) := c1;
                ret (2) := c1;
                ret (3) := c1;
                size    := 3;
            when 4 =>
                ret (1) := c1;
                ret (2) := c2;
                size    := 2;
            when 5 =>
                ret (1) := c2;
                size    := 1;
            when 6 =>
                ret (1) := c2;
                ret (2) := c1;
                size    := 2;
            when 7 =>
                ret (1) := c2;
                ret (2) := c1;
                ret (3) := c1;
                size    := 3;
            when 8 =>
                ret (1) := c2;
                ret (2) := c1;
                ret (3) := c1;
                ret (4) := c1;
                size    := 4;
            when 9 =>
                ret (1) := c1;
                ret (2) := c3;
                size    := 2;
        end case;

        return ret (1 .. size);
    end DigitToString;

    function IntToStringRoman(n: RomanNumber) return String is
    ret : String(1..10)
    begin
    end IntToStringRoman;
begin
    -- Test DigitToString
    pragma Assert (DigitToString (0, 'I', 'V', 'X') = "");
    pragma Assert (DigitToString (1, 'I', 'V', 'X') = "I");
    pragma Assert (DigitToString (2, 'I', 'V', 'X') = "II");
    pragma Assert (DigitToString (3, 'I', 'V', 'X') = "III");
    pragma Assert (DigitToString (4, 'I', 'V', 'X') = "IV");
    pragma Assert (DigitToString (5, 'I', 'V', 'X') = "V");
    pragma Assert (DigitToString (6, 'I', 'V', 'X') = "VI");
    pragma Assert (DigitToString (7, 'I', 'V', 'X') = "VII");
    pragma Assert (DigitToString (8, 'I', 'V', 'X') = "VIII");
    pragma Assert (DigitToString (9, 'I', 'V', 'X') = "IX");
end Exo4;
