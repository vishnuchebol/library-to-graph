import ast
import pathlib
import networkx as nx


def find_calls(func_node):
    """Yield all function names that are called inside this function."""
    for node in ast.walk(func_node):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                yield node.func.id
            elif isinstance(node.func, ast.Attribute):
                yield node.func.attr  # catches method calls like obj.method()

def process_file(file_path, graph):
    try:
        tree = ast.parse(file_path.read_text(encoding="utf-8"), filename=str(file_path))
    except Exception as e:
        print(f"Skipping {file_path} due to parse error: {e}")
        return

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            func_name = f"{file_path.name}__{node.name}"  # Avoid ":" to prevent pydot issues
            for callee in find_calls(node):
                graph.add_edge(func_name, callee)

def build_callgraph():
    g = nx.DiGraph()

    FILES_TO_ANALYZE = [
        pathlib.Path(r"C:\Users\vishn\OneDrive - BIRLA INSTITUTE OF TECHNOLOGY and SCIENCE\Desktop\Nemo\NeMo\nemo\collections\asr\data\audio_to_text.py"),
        pathlib.Path(r"C:\Users\vishn\OneDrive - BIRLA INSTITUTE OF TECHNOLOGY and SCIENCE\Desktop\Nemo\NeMo\nemo\collections\asr\losses\ctc.py"),
        pathlib.Path(r"C:\Users\vishn\OneDrive - BIRLA INSTITUTE OF TECHNOLOGY and SCIENCE\Desktop\Nemo\NeMo\nemo\collections\asr\metrics\wer.py"),
        pathlib.Path(r"C:\Users\vishn\OneDrive - BIRLA INSTITUTE OF TECHNOLOGY and SCIENCE\Desktop\Nemo\NeMo\nemo\collections\asr\models\ctc_models.py"),
    ]

    for pyfile in FILES_TO_ANALYZE:
        process_file(pyfile.resolve(), g)

    nx.nx_pydot.write_dot(g, "callgraph2.dot")
    print("✅ Call graph written to 'callgraph2.dot'. To render it as a PNG, run:")
    print("   dot -Tpng callgraph2.dot -o callgraph2.png")

if __name__ == "__main__":
    build_callgraph()
