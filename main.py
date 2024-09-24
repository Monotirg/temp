from easy_tree import Tree


root = r"D:\Projects"
tree = Tree.load_dir(root)

with open("temp.json", "w+", encoding="utf-8") as f:
    f.write(tree.to_json())