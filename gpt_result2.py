import subprocess
import json

def execute_command(command, check_returncode=True):
    """コマンドを実行してその出力を返す関数"""
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    return result.stdout.strip()

def pretty_json(branch, file_path):
    """ブランチ内のJSONファイルを整形して返す"""
    raw_json = execute_command(f"git show {branch}:{file_path}")
    parsed_json = json.loads(raw_json)
    return json.dumps(parsed_json, indent=4)

def get_diff(base_branch, feature_branch, file_path):
    """指定したブランチ間の指定されたファイルの差分を取得"""
    base_contents = pretty_json(base_branch, file_path)
    feature_contents = pretty_json(feature_branch, file_path)

    with open("base.json", "w") as f:
        f.write(base_contents)

    with open("feature.json", "w") as f:
        f.write(feature_contents)

    diff = execute_command(f"diff base.json feature.json")
    execute_command("rm base.json feature.json")

    return diff

def apply_diff_to_branch(target_branch, diff):
    """差分を指定したブランチに適用する関数"""
    with open("temp_diff.txt", "w") as f:
        f.write(diff)

    execute_command(f"git checkout {target_branch}")
    execute_command(f"git apply temp_diff.txt")
    
    # ファイルを再び一行のJSONとして保存
    with open(json_file_path, "r") as f:
        data = json.load(f)

    with open(json_file_path, "w") as f:
        f.write(json.dumps(data))

    execute_command(f"git add .")
    execute_command(f"git commit -m 'Applied changes from diff'")
    execute_command("rm temp_diff.txt")

if __name__ == "__main__":
    BASE_BRANCH = 'main'
    FEATURE_BRANCH = 'a_branch'

    json_file_path = "./project.json"  # JSONファイルのパスを設定

    # Bブランチの差分をAブランチにマージ
    diff_B_to_A = get_diff(BASE_BRANCH, FEATURE_BRANCH, json_file_path)
    apply_diff_to_branch(BASE_BRANCH, diff_B_to_A)

    # Aブランチの差分をmainブランチにマージ
    # diff_A_to_main = get_diff("main", "A", json_file_path)
    # apply_diff_to_branch("main", diff_A_to_main)