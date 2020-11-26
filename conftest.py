import platform


win_broken_cmd = 'clear', 'login', 'watch'

win_broken = [f'cmdix/command/{cmd}.py' for cmd in win_broken_cmd] + [
    'cmdix/test/test_login.py'
]


collect_ignore = win_broken if platform.system() == 'Windows' else []
