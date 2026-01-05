def print_tree(node, indent=0):

    prefix = "|  " * indent

    if isinstance(node, list):
        for elem in node:
            print_tree(elem, indent)
        return

    if isinstance(node, (int, float)):
        print(prefix + str(node))
        return

    if isinstance(node, str):
        print(prefix + node)
        return

    if isinstance(node, tuple):
        if len(node) == 0:
            print(prefix + "EMPTY")
            return

        tag = node[0]

        if tag == 'assign':
            print(prefix + "=")
            target = node[1]
            expr = node[2]
            print_tree(target, indent + 1)
            print_tree(expr, indent + 1)
            return

        if tag in ('zeros', 'ones', 'eye'):
            print(prefix + tag)
            args = node[1]
            print_tree(args, indent + 1)
            return

        if tag == 'transpose':
            print(prefix + "TRANSPOSE")
            print_tree(node[1], indent + 1)
            return

        if tag == 'index':
            print(prefix + "INDEX")
            print_tree(node[1], indent + 1)
            return

        if tag == 'matrix':
            print(prefix + "VECTOR")
            payload = node[1]

            rows = _extract_matrix_rows(payload)
            for row in rows:
                print(prefix + "|  VECTOR")
                print_tree(row, indent + 2)
            return

        if tag == 'block':
            print_tree(node[1], indent)
            return

        if tag in ('+', '-', '*', '/', 'DOTADD', 'DOTSUB', 'DOTMUL', 'DOTDIV',
                   '>', '<', 'LESSEQ', 'MOREEQ', 'EQUALS', 'NOTEQ', 'range'):
            op = _map_op(tag)
            print(prefix + op)
            print_tree(node[1], indent + 1)
            print_tree(node[2], indent + 1)
            return

        if isinstance(tag, str) and len(node) == 2 and isinstance(node[1], tuple) and node[1][0] == 'index':
            print(prefix + "REF")
            print(prefix + "|  " + tag)
            print_tree(node[1], indent + 1)
            return

        print(prefix + str(tag))
        for child in node[1:]:
            print_tree(child, indent + 1)
        return

    print(prefix + repr(node))


def _map_op(op):
    mapping = {
        'DOTADD': '.+',
        'DOTSUB': '.-',
        'DOTMUL': '.*',
        'DOTDIV': './',
        'LESSEQ': '<=',
        'MOREEQ': '>=',
        'EQUALS': '==',
        'NOTEQ': '!=',
        'range': 'RANGE',
    }
    return mapping.get(op, op)


def _extract_matrix_rows(payload):
    rows = []

    def walk(x):
        if isinstance(x, list):
            if all(isinstance(v, (int, float)) for v in x):
                rows.append(x)
            else:
                for v in x:
                    walk(v)
            return

        if isinstance(x, tuple):
            if len(x) >= 2 and x[0] == 'matrix':
                for v in x[1:]:
                    walk(v)
            else:
                for v in x:
                    walk(v)
            return

    walk(payload)

    if not rows and isinstance(payload, list):
        rows = [payload]

    return rows
