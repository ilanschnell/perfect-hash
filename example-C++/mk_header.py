for line in open('states.dat'):
    line = line.strip()
    if line.startswith('#'):
        continue

    row = tuple(entry.strip() for entry in line.split('|'))

    print('  {"%s", "%s", %s},' % row)
