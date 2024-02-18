
from flowhigh.model.TypeCast import TypeCast
from flowhigh.model.TreeNode import TreeNode


class AntiPattern(TypeCast, TreeNode):
    severity: str = None
    readability: str = None
    correctness: str = None
    performance: str = None
    pos: list = []
    link: str = None
    type_: str = None
    
    name: str = None
    

    def __init__(self):
        super().__init__()



from flowhigh.model.TreeNode import TreeNode

class AntiPatternBuilder (object):
    construction: AntiPattern
    
    ap_links: dict = {'AP_01': {'name': 'AP 01 - Avoid ANSI-89 join syntax', 'severity': 'Warning', 'performance': ' ', 'readability': 'Y', 'correctness': ' ', 'link': 'https://docs.sonra.io/flowhigh/master/docs/sql-analyser/sql-anti-patterns/avoid-ansi-89-join-syntax/'}, 'AP_02': {'name': 'AP 02 - Beware of count distinct', 'severity': 'Notice', 'performance': 'Y', 'readability': ' ', 'correctness': ' ', 'link': 'https://docs.sonra.io/flowhigh/master/docs/sql-analyser/sql-anti-patterns/beware-of-count-distinct/'}, 'AP_03': {'name': 'AP 03 - Avoid count(*) in the outer join', 'severity': 'Warning', 'performance': 'Y', 'readability': ' ', 'correctness': 'Y', 'link': 'https://docs.sonra.io/flowhigh/master/docs/sql-analyser/sql-anti-patterns/avoid-count-in-the-outer-join/'}, 'AP_04': {'name': 'AP 04 - Avoid nesting scalar subqueries in the SELECT statement', 'severity': 'Warning', 'performance': 'Y', 'readability': 'Y', 'correctness': 'Y', 'link': 'https://docs.sonra.io/flowhigh/master/docs/sql-analyser/sql-anti-patterns/avoid-nesting-scalar-subqueries-in-the-select-statement/'}, 'AP_05': {'name': 'AP 05 - Beware of SELECT *', 'severity': 'Caution', 'performance': 'Y', 'readability': 'Y', 'correctness': ' ', 'link': 'https://docs.sonra.io/flowhigh/master/docs/sql-analyser/sql-anti-patterns/beware-of-select-star/'}, 'AP_06': {'name': 'AP 06 - Beware of SELECT DISTINCT', 'severity': 'Notice', 'performance': 'Y', 'readability': ' ', 'correctness': 'Y', 'link': 'https://docs.sonra.io/flowhigh/master/docs/sql-analyser/sql-anti-patterns/beware-of-select-distinct/'}, 'AP_07': {'name': 'AP 07 - Avoid using functions in the WHERE clause', 'severity': 'Caution', 'performance': 'Y', 'readability': ' ', 'correctness': ' ', 'link': 'https://docs.sonra.io/flowhigh/master/docs/sql-analyser/sql-anti-patterns/avoid-using-functions-in-the-where-clause/'}, 'AP_08': {'name': 'AP 08 - Beware of NULL with arithmetic and string operations', 'severity': 'Caution', 'performance': ' ', 'readability': ' ', 'correctness': 'Y', 'link': 'https://docs.sonra.io/flowhigh/master/docs/sql-analyser/sql-anti-patterns/beware-of-null-with-arithmetic-and-string-operations/'}, 'AP_09': {'name': 'AP 09 - Avoid filtering attributes from the non-preserved side of an outer join', 'severity': 'Warning', 'performance': ' ', 'readability': ' ', 'correctness': 'Y', 'link': 'https://docs.sonra.io/flowhigh/master/docs/sql-analyser/sql-anti-patterns/avoid-filtering-attributes-from-the-non-preserved-side-of-an-outer-join/'}, 'AP_10': {'name': 'AP 10 - Beware of filtering for NULL', 'severity': 'Warning', 'performance': ' ', 'readability': ' ', 'correctness': 'Y', 'link': 'https://docs.sonra.io/flowhigh/master/docs/sql-analyser/sql-anti-patterns/beware-of-filtering-for-null/'}, 'AP_11': {'name': 'AP 11 - Avoid implicit column references', 'severity': 'Warning', 'performance': ' ', 'readability': 'Y', 'correctness': 'Y', 'link': 'https://docs.sonra.io/flowhigh/master/docs/sql-analyser/sql-anti-patterns/avoid-implicit-column-references/'}, 'AP_12': {'name': 'AP 12 - Beware of implicit self-joins in a correlated subquery', 'severity': 'Caution', 'performance': 'Y', 'readability': 'Y', 'correctness': ' ', 'link': 'https://docs.sonra.io/flowhigh/master/docs/sql-analyser/sql-anti-patterns/beware-of-implicit-self-joins-in-a-correlated-subquery/'}, 'AP_13': {'name': 'AP 13 - Avoid inner join after outer join in multi-join query', 'severity': 'Warning', 'performance': ' ', 'readability': ' ', 'correctness': 'Y', 'link': 'https://docs.sonra.io/flowhigh/master/docs/sql-analyser/sql-anti-patterns/avoid-inner-join-after-outer-join-in-multi-join-query/'}, 'AP_14': {'name': 'AP 14 - Avoid implicit cross join', 'severity': 'Warning', 'performance': ' ', 'readability': 'Y', 'correctness': 'Y', 'link': 'https://docs.sonra.io/flowhigh/master/docs/sql-analyser/sql-anti-patterns/avoid-implicit-cross-join/'}, 'AP_15': {'name': 'AP 15 - Use an alias for derived columns', 'severity': 'Warning', 'performance': ' ', 'readability': 'Y', 'correctness': ' ', 'link': 'https://docs.sonra.io/flowhigh/master/docs/sql-analyser/sql-anti-patterns/use-an-alias-for-derived-columns/'}, 'AP_16': {'name': 'AP 16 - Beware of NULL in combination with not equal operator (!=, <>)', 'severity': 'Warning', 'performance': ' ', 'readability': ' ', 'correctness': 'Y', 'link': 'https://docs.sonra.io/flowhigh/master/docs/sql-analyser/sql-anti-patterns/beware-of-null-in-combination-with-not-equal-operator/'}, 'AP_17': {'name': 'AP 17 - Use IN / NOT IN for multiple OR operators', 'severity': 'Caution', 'performance': ' ', 'readability': 'Y', 'correctness': ' ', 'link': 'https://docs.sonra.io/flowhigh/master/docs/sql-analyser/sql-anti-patterns/use-in-or-not-in-for-multiple-or-operators/'}, 'AP_18': {'name': 'AP 18 - Avoid ordinal numbers when using ORDER BY or GROUP BY', 'severity': 'Caution', 'performance': ' ', 'readability': 'Y', 'correctness': 'Y', 'link': 'https://docs.sonra.io/flowhigh/master/docs/sql-analyser/sql-anti-patterns/avoid-ordinal-numbers-when-using-order-by-or-group-by/'}, 'AP_19': {'name': 'AP 19 - Split multi join queries into smaller chunks', 'severity': 'Caution', 'performance': 'Y', 'readability': 'Y', 'correctness': ' ', 'link': 'https://docs.sonra.io/flowhigh/master/docs/sql-analyser/sql-anti-patterns/split-multi-join-queries-into-smaller-chunks/'}, 'AP_20': {'name': 'AP 20 - Avoid unused Common Table Expressions (CTE)', 'severity': 'Warning', 'performance': 'Y', 'readability': 'Y', 'correctness': ' ', 'link': 'https://docs.sonra.io/flowhigh/master/docs/sql-analyser/sql-anti-patterns/avoid-unused-common-table-expressions-cte/'}, 'AP_21': {'name': 'AP 21 - Use window functions instead of self joins', 'severity': 'Caution', 'performance': 'Y', 'readability': 'Y', 'correctness': ' ', 'link': 'https://docs.sonra.io/flowhigh/master/docs/sql-analyser/sql-anti-patterns/use-window-functions-instead-of-self-joins/'}, 'AP_22': {'name': 'AP 22 - Avoid UNION for multiple filter values', 'severity': 'Caution', 'performance': 'Y', 'readability': 'Y', 'correctness': ' ', 'link': 'https://docs.sonra.io/flowhigh/master/docs/sql-analyser/sql-anti-patterns/avoid-union-for-multiple-filter-values/'}, 'AP_23': {'name': 'AP 23 - Avoid the natural join clause', 'severity': 'Warning', 'performance': ' ', 'readability': 'Y', 'correctness': 'Y', 'link': 'https://docs.sonra.io/flowhigh/master/docs/sql-analyser/sql-anti-patterns/avoid-the-natural-join-clause/'}, 'AP_24': {'name': 'AP 24 - Use LIKE instead of REGEX where LIKE is possible', 'severity': 'Warning', 'performance': 'Y', 'readability': ' ', 'correctness': ' ', 'link': 'https://docs.sonra.io/flowhigh/master/docs/sql-analyser/sql-anti-patterns/use-like-instead-of-regex-where-like-is-possible/'}, 'AP_25': {'name': 'AP 25 - Use UNION ALL instead of UNION', 'severity': 'Caution', 'performance': 'Y', 'readability': ' ', 'correctness': ' ', 'link': 'https://docs.sonra.io/flowhigh/master/docs/sql-analyser/sql-anti-patterns/use-union-all-instead-of-union/'}, 'AP_26': {'name': 'AP 26 - Avoid using WHERE to filter aggregate columns', 'severity': 'Warning', 'performance': 'Y', 'readability': 'Y', 'correctness': ' ', 'link': 'https://docs.sonra.io/flowhigh/master/docs/sql-analyser/sql-anti-patterns/avoid-using-where-to-filter-aggregate-columns/'}, 'AP_27': {'name': 'AP 27 - Use an alias for inline views', 'severity': 'Caution', 'performance': ' ', 'readability': 'Y', 'correctness': ' ', 'link': 'https://docs.sonra.io/flowhigh/master/docs/sql-analyser/sql-anti-patterns/use-an-alias-for-inline-views/'}, 'AP_28': {'name': 'AP 28 - Avoid using functions in the Join clause', 'severity': 'Caution', 'performance': 'Y', 'readability': ' ', 'correctness': ' ', 'link': 'https://docs.sonra.io/flowhigh/master/docs/sql-analyser/sql-anti-patterns/avoid-using-functions-in-the-join-clause/'}, 'AP_29': {'name': 'AP 29 - Use parentheses when mixing ANDs with ORs', 'severity': 'Caution', 'performance': ' ', 'readability': 'Y', 'correctness': ' ', 'link': 'https://docs.sonra.io/flowhigh/master/docs/sql-analyser/sql-anti-patterns/use-parentheses-when-mixing-ands-with-ors/'}, 'AP_30': {'name': 'AP 30 - Avoid or delay ORDER BY in inline views', 'severity': 'Caution', 'performance': 'Y', 'readability': ' ', 'correctness': ' ', 'link': 'https://docs.sonra.io/flowhigh/master/docs/sql-analyser/sql-anti-patterns/avoid-or-delay-order-by-in-inline-views/'}, 'AP_33': {'name': 'AP 33 - WHERE NOT IN without NOT NULL check in subquery', 'severity': 'Caution', 'performance': ' ', 'readability': ' ', 'correctness': 'Y', 'link': 'https://docs.sonra.io/flowhigh/master/docs/sql-analyser/sql-anti-patterns/where-not-in-without-not-null-check-in-subquery/'}, 'AP_34': {'name': 'AP 34 - Pseudo join condition results in a CROSS join.', 'severity': 'Notice', 'performance': 'Y', 'readability': ' ', 'correctness': 'Y', 'link': 'https://docs.sonra.io/flowhigh/master/docs/sql-analyser/sql-anti-patterns/pseudo-join-condition-results-in-a-cross-join/'}, 'AP_36': {'name': 'AP 36 - JOIN condition linking the compound key to multiple, different tables.', 'severity': 'Caution', 'performance': 'Y', 'readability': ' ', 'correctness': 'Y', 'link': 'https://docs.sonra.io/flowhigh/master/docs/sql-analyser/sql-anti-patterns/join-condition-linking-the-compound-key-to-multiple-different-tables/'}, 'AP_38': {'name': 'AP 38 - Avoid nested CTEs', 'severity': 'Notice', 'performance': ' ', 'readability': 'Y', 'correctness': ' ', 'link': 'https://docs.sonra.io/flowhigh/master/docs/sql-analyser/sql-anti-patterns/avoid-nested-ctes/'}}

    def with_name(self, type: str):
        if isinstance(type, str) and type.startswith("AP_"):
            child = self.ap_links[type]["name"]
        else:
            child = None
        self.construction.name = child
    

    def __init__(self) -> None:
        super().__init__()
        self.construction = AntiPattern()
    
    def with_severity(self, severity: str):
        if isinstance(severity, str) and severity.startswith("AP_"):
            child = self.ap_links[severity]["severity"]
        else:
            child = None
        self.construction.severity = child
    
    def with_readability(self, readability: str):
        if isinstance(readability, str) and readability.startswith("AP_"):
            child = self.ap_links[readability]["readability"]
        else:
            child = None
        self.construction.readability = child
    
    def with_correctness(self, correctness: str):
        if isinstance(correctness, str) and correctness.startswith("AP_"):
            child = self.ap_links[correctness]["correctness"]
        else:
            child = None
        self.construction.correctness = child
    
    def with_performance(self, performance: str):
        if isinstance(performance, str) and performance.startswith("AP_"):
            child = self.ap_links[performance]["performance"]
        else:
            child = None
        self.construction.performance = child
    
    def with_pos(self, pos: list):
        child = pos
        for node in list(filter(lambda el: TreeNode in el.__class__.mro(), pos)):
            self.construction.add_child(node)
        self.construction.pos = child
    
    def with_link(self, link: str):
        if isinstance(link, str) and link.startswith("AP_"):
            child = self.ap_links[link]["link"]
        else:
            child = None
        self.construction.link = child
    
    def with_type(self, type_: str):
        child = type_
        self.construction.type_ = child

    def build(self):
        return self.construction
