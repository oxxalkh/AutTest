import re
import subprocess
import re

if __name__ == '__main__':
    def check_output(command, text, del_punct=False):
        try:
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding="utf-8")
            out = result.stdout
            if result.returncode == 0 and del_punct:

                lst = re.findall(r'\w+', out)
                print(lst)
                if text in lst:
                    return f"{text} caught "
                else:
                    return "Fail1"
            elif result.returncode == 0:
                if text in out:
                    return f"{text} caught"
                else:
                    return "Fail2"
            else:
                return "Fail3"

        except subprocess.CalledProcessError:
            return False


print(check_output('ls', 'task01', True))
