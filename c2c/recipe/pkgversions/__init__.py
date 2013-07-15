# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE
from os import environ
from zc.buildout import UserError
from pkg_resources import parse_version


class PkgVersions(object):

    def __init__(self, buildout, name, options):
        env = environ
        if 'PATH' not in env:
            env = env.copy()
            env['PATH'] = '/usr/bin:/bin'

        p = Popen(['dpkg', '-l'], stdout=PIPE, env=env)
#        p.wait()
        versions = {}
        for line in p.stdout.readlines():
            pkg = line.split()
            # ignore title and get inly installed
            if len(pkg) > 2 and pkg[0] == 'ii':
                versions[pkg[1].split(':')[0]] = pkg[2]

        errors = []
        for p, v in options.items():
            if p != 'recipe':
                if not p in versions:
                    errors.append(
                        'The package %(p)s is not installed.' % {
                            'p': p,
                        }
                    )
                elif parse_version(versions[p]) < parse_version(v):
                    errors.append(
                        ('The package %(p)s is on version %(av)s and he ' +
                            'should be at least %(rv)s.') % {
                                'p': p,
                                'av': versions[p],
                                'rv': v,
                            }
                    )

        if len(errors) > 0:
            raise UserError('\n'.join(errors))

    def install(self):
        return ()

    update = install
