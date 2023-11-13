import subprocess

tst = "/home/user/tst"
out = "/home/user/out"
folder1 = "/home/user/folder1"
folder2 = "/home/user/folder2"


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if text in result.stdout and result.returncode == 0:
        return True
    else:
        return False


def checkhash(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    return result.stdout.upper()


def test_step1():
    # test1
    result1 = checkout("cd {}; 7z a {}/arx2".format(tst, out), "Everything is Ok")
    result2 = checkout("cd {}; ls".format(out), "arx2.7z")
    assert result1 and result2, "test1 FAIL"


def test_step2():
    # test2
    result1 = checkout("cd {}; 7z e arx2.7z -o{} -y".format(out, folder1), "Everything is Ok")
    result2 = checkout("cd {}; ls".format(folder1), "qwe")
    result3 = checkout("cd {}; ls".format(folder1), "qwa")
    result4 = checkout("cd {}; ls".format(folder1), "add")
    assert result1 and result2 and result3 and result4, "test2 FAIL"


def test_step3():
    # test3
    assert checkout("cd {}; 7z t arx2.7z ".format(out), "Everything is Ok"), "test3 FAIL"


def test_step4():
    # test4
    assert checkout("cd {}; 7z u {}/arx2.7z ".format(tst, out), "Everything is Ok"), "test4 FAIL"


def test_step5():
    # test5
    result1 = checkout("cd {}; 7z l arx2.7z".format(out), "qwe")
    result2 = checkout("cd {}; 7z l arx2.7z".format(out), "qwa")
    result3 = checkout("cd {}; 7z l arx2.7z".format(out),  "add")
    assert result1 and result2 and result3, "test5 FAIL"


def test_step7():
    # test7
    result1 = checkout("cd {}; 7z x arx2.7z -o{} -y".format(out, folder2), "Everything is Ok")
    result2 = checkout("ls {}".format(folder2), "qwe")
    result3 = checkout("ls {}".format(folder2), "qwa")
    result4 = checkout("ls {}".format(folder2), "add")

    assert result1 and result2 and result3 and result4,  "test6 FAIL"


def test_step8():
    # test8
    result1 = checkout("cd {}; 7z h qwe".format(tst), "Everything is Ok")
    print(result1)
    result2 = checkout("cd {}; 7z h qwe".format(tst), checkhash("cd {}; crc32 qwe".format(tst)))
    print(result2)

    assert result1 and result2, "test8 FAIL"


def test_step9():
    # test9
    assert checkout("cd {}; 7z d {}/arx2.7z ".format(out, out), "Everything is Ok"), "test9 FAIL"

