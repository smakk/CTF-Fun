import angr
def main():
	proj = angr.Project('./baby-re',  load_options={'auto_load_libs': False})
	path_group = proj.factory.path_group()
	path_group.explore(find=0x40294b, avoid=0x402941)
        print path_group.found[0].state.posix.dumps(0)
	return path_group.found[0].state.posix.dumps(1)
if __name__ == '__main__':
	print(repr(main()))
