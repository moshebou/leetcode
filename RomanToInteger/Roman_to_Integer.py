class Solution(object):
    def romanToInt(self, s):
        """
        :type s: str
        :rtype: int
        """
        sym_to_val = {  "I":(1, "-"),
                        "V":(5, "I"),
                        "X":(10, "I"),
                        "L":(50, "X"),
                        "C":(100, "X"),
                        "D":(500, "C"),
                        "M":(1000, "C")}
        prev = None
        val = 0
        for item in s:
            if prev == sym_to_val[item][1]:
                val -= 2*sym_to_val[prev][0]
            val += sym_to_val[item][0]
            prev = item

        return val