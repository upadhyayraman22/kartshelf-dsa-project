"""
dsa/trie.py - Prefix Trie (Retrieval Tree) for Autocomplete
Implemented from scratch without external regex or prefix shortcuts.

Classes:
1. TrieNode: Multi-way prefix character node.
2. Trie: As-you-type search autocomplete engine with prefix highlighting.
"""

from typing import Any, List, Optional, Dict, Tuple


class TrieNode:
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end_of_word: bool = False
        self.products: List[Any] = []  # Can hold multiple products sharing exact same search token


class Trie:
    """
    Prefix Trie (Digital Search Tree).
    
    Purpose:
        Powers search box autocomplete (as-you-type) with matched prefix highlighting.
    Operations:
        - insert(word, product_data): O(L) where L is length of word.
        - search(word): O(L)
        - starts_with(prefix): O(L)
        - autocomplete(prefix, limit): O(L + K) where K is number of descendants.
        - delete(word): O(L)
    """

    def __init__(self):
        self.root = TrieNode()
        self.word_count = 0

    def insert(self, word: str, product_data: Any = None) -> None:
        if not word:
            return

        curr = self.root
        clean_word = word.lower().strip()

        for char in clean_word:
            if char not in curr.children:
                curr.children[char] = TrieNode()
            curr = curr.children[char]

        if not curr.is_end_of_word:
            curr.is_end_of_word = True
            self.word_count += 1

        if product_data is not None:
            curr.products.append(product_data)

    def search(self, word: str) -> bool:
        curr = self.root
        clean_word = word.lower().strip()
        for char in clean_word:
            if char not in curr.children:
                return False
            curr = curr.children[char]
        return curr.is_end_of_word

    def delete(self, word: str) -> bool:
        clean_word = word.lower().strip()
        deleted = False

        def _delete(node: TrieNode, word_str: str, index: int) -> bool:
            nonlocal deleted
            if index == len(word_str):
                if not node.is_end_of_word:
                    return False
                node.is_end_of_word = False
                node.products = []
                self.word_count -= 1
                deleted = True
                return len(node.children) == 0

            char = word_str[index]
            if char not in node.children:
                return False

            can_delete_child = _delete(node.children[char], word_str, index + 1)

            if can_delete_child:
                del node.children[char]
                return len(node.children) == 0 and not node.is_end_of_word

            return False

        _delete(self.root, clean_word, 0)
        return deleted

    def autocomplete(self, prefix: str, limit: int = 6) -> List[Dict[str, Any]]:
        """
        Returns completions for prefix with highlighted token segmentation.
        Output format:
        [
            {
                "prefix": "air",
                "suffix": "dopes 441 tws earbuds",
                "full_word": "airdopes 441 tws earbuds",
                "products": [...]
            }
        ]
        """
        clean_prefix = prefix.lower().strip()
        curr = self.root

        # Step 1: Traverse to end of prefix
        for char in clean_prefix:
            if char not in curr.children:
                return []
            curr = curr.children[char]

        # Step 2: DFS collect all words beneath prefix
        results: List[Dict[str, Any]] = []

        def _collect(node: TrieNode, path_chars: List[str]):
            if len(results) >= limit:
                return

            if node.is_end_of_word:
                suffix = "".join(path_chars)
                results.append({
                    "prefix": clean_prefix,
                    "suffix": suffix,
                    "full_word": clean_prefix + suffix,
                    "products": node.products[:2]  # return top products
                })

            # Sort children keys for deterministic alphabetical output
            # Manual sorting of keys:
            child_keys = list(node.children.keys())
            for i in range(len(child_keys)):
                for j in range(i + 1, len(child_keys)):
                    if child_keys[i] > child_keys[j]:
                        child_keys[i], child_keys[j] = child_keys[j], child_keys[i]

            for char in child_keys:
                path_chars.append(char)
                _collect(node.children[char], path_chars)
                path_chars.pop()

        _collect(curr, [])
        return results

    def to_tree_dict(self, node: Optional[TrieNode] = None, char_label: str = "root", depth: int = 0) -> Optional[Dict[str, Any]]:
        if depth > 4:  # Bounded depth for JSON visualization payload
            return None
        if node is None:
            node = self.root

        children_dict = []
        for char, child in node.children.items():
            cd = self.to_tree_dict(child, char, depth + 1)
            if cd:
                children_dict.append(cd)

        return {
            "name": f"'{char_label}'" + (" [Word]" if node.is_end_of_word else ""),
            "char": char_label,
            "is_word": node.is_end_of_word,
            "children": children_dict
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "Trie",
            "word_count": self.word_count,
            "tree": self.to_tree_dict()
        }
