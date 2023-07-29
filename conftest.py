import platform


win_broken_cmd = 'clear', 'watch'

win_broken = [f'cmdix/command/{cmd}.py' for cmd in win_broken_cmd]


collect_ignore = win_broken if platform.system() == 'Windows' else []
