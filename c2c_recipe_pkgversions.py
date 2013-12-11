# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE
from os import environ
from zc.buildout import UserError
from pkg_resources import parse_version


class PkgVersions(object):

    def __init__(self, buildout, name, options):
        self.env = environ
        if 'PATH' not in self.env:
            self.env = self.env.copy()
            self.env['PATH'] = '/usr/bin:/bin'

        p = Popen(['dpkg', '--list'], stdout=PIPE, env=self.env)
        self.versions = {}
        for line in p.stdout.readlines():
            pkg = line.split()
            # ignore title and get only installed
            if len(pkg) > 2 and pkg[0] == 'ii':
                self.versions[pkg[1].split(':')[0]] = pkg[2]

        errors = []
        for p, v in options.items():
            if p != 'recipe':
                err = self.test_package(p, v)
                if err is not None:
                    errors.append(err)

        if len(errors) > 0:
            raise UserError('\n'.join(errors))

    def test_package(self, package, version, can_be_virtual=True):
        if version == 'installed':
            version = 'dev'
        if version == '':
            return None
        elif version == 'not-installed':
            if package in self.versions:
                ''
                return 'The package %(p)s is installed but he shouldni\'t.' % {
                    'p': package,
                }
            else:
                return None
        elif not package in self.versions:
            found = False
            if can_be_virtual:
                p = Popen(['apt-cache', 'showpkg', package], stdout=PIPE, env=self.env)
                in_reverse_provides = False
                for line in p.stdout.readlines():
                    l = line.strip()
                    if len(l) > 0 and l[-1] == ':':
                        in_reverse_provides = l == 'Reverse Provides:'
                    elif in_reverse_provides:
                        err = self.test_package(line.split()[0], version, False)
                        if err is None:
                            found = True

            if not found:
                return 'The package %(p)s is not installed.' % {
                    'p': package,
                }

        elif parse_version(self.versions[package]) < parse_version(version):
            return ('The package %(p)s is on version %(av)s and he ' +
                    'should be at least %(rv)s.') % {
                'p': package,
                'av': self.versions[package],
                'rv': version,
                }
        return None

    def install(self):
        return ()

    update = install
