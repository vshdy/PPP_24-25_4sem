class Node:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(data):
    from heapq import heappush, heappop, heapify
    freq = {ch: data.count(ch) for ch in set(data)}
    heap = [Node(ch, freq[ch]) for ch in freq]
    heapify(heap)
    while len(heap) > 1:
        a, b = heappop(heap), heappop(heap)
        parent = Node(freq=a.freq + b.freq)
        parent.left, parent.right = a, b
        heappush(heap, parent)
    return heap[0]

def build_code_table(node, prefix="", table=None):
    if table is None:
        table = {}
    if node.char is not None:
        table[node.char] = prefix
    else:
        build_code_table(node.left, prefix + "0", table)
        build_code_table(node.right, prefix + "1", table)
    return table

def huffman_encode(data):
    tree = build_huffman_tree(data)
    table = build_code_table(tree)
    return ''.join(table[c] for c in data), table

def huffman_decode(bits, table):
    reverse = {v: k for k, v in table.items()}
    buffer, result = '', ''
    for bit in bits:
        buffer += bit
        if buffer in reverse:
            result += reverse[buffer]
            buffer = ''
    return result
