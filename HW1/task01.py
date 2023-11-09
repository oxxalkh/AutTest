import subprocess

if __name__ == '__main__':
    def check_output(command, text):
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding="utf-8")
        out = result.stdout
        try:
            if result.returncode == 0:
                lst = out.split("\n")
                if text in lst:
                    return True
                else:
                    False
        except subprocess.CalledProcessError:
            return False


print(check_output('ls', 'task01.py'))
